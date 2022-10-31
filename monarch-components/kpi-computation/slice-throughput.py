import requests
import pandas as pd
import json

# disable annoying warning message
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)

PROMETHEUS_URL = "http://129.97.168.51:30090"
ELASTICSEARCH_URL = "https://129.97.26.28:31920/"
ELASTIC_INDEX = "logstash-filebeat"  # this index stores slice information from the SMF
ELASTIC_QUERY_URL = ELASTICSEARCH_URL + ELASTIC_INDEX + "/_search?pretty=true&filter_path=hits.hits*"

# PARAMS = {'query': "pdr_packet_count"}  # get last data point (instant vector)
PROM_PARAMS = {'query': 'deriv(pdr_byte_count[10s])'}  # per-second derivative of range vector

ES_PARAMS = {   
    "size": 50,
    "sort": { "@timestamp": "desc"},
    "_source": "false",
    "query" : {
            "match_all" : {}
        },
        "fields": ["S-NSSAI", "slice-session-info.PFCPSession.PDRs.PDRId", "slice-session-info.PFCPSession.PDRs.Fteid.GTPIPAddress", "slice-session-info.PFCPSession.Fseid.LocalSEID","slice-session-info.PFCPSession.Fseid.IPAddress", "slice-session-info.PduSession.DataNetworkName"]
}

HEADERS = {'Content-type': 'application/json'}


def sanitize_prometheus_response(data):
    """ Take a prometheus result and transform it into a pandas dataframe """
    result = data["data"]["result"]

    d_list = []  # list of dict, where each dict is a row in pandas dataframe
    for item in result:
        d = {}
        labels = item["metric"]
        d["direction"] = labels["direction"]
        d["pdrid"] = int(labels["pdrid"])
        d["seid"] = int(labels["seid"])
        d["value"] = float(item["value"][1])
        d["n3_ipaddr"] = labels["n3_ipaddr"]
        d["n4_ipaddr"] = labels["n4_ipaddr"]
        d_list.append(d)

    df = pd.DataFrame(d_list)
    return df

def sanitize_elastic_response(result):
    """ Sanitize Elasticsearch result and transform it into a Pandas dataframe """

    # drop useless columns
    df = pd.json_normalize(result["hits"]["hits"]).drop(columns=["_index", "_id", "_score", "_ignored", "sort"])

    # rename columns to make them easier to work with
    df.columns = ["n3_ipaddr", "dnn", "seid", "n4_ipaddr", "snssai", "pdrid"]

    def sanitize_column(col):
        """ Each col is a list containting a single element. Extract the element """
        df[col] = df[col].apply(lambda x: next(s for s in x if s))

    sanitize_column("dnn")
    sanitize_column("n3_ipaddr")
    sanitize_column("seid")
    sanitize_column("n4_ipaddr")
    sanitize_column("snssai")

    df = df.explode("pdrid")
    return df

def send_queries():
    """ send queries to both Elastic and Prometheus to collect necessary data for slice throughput KPI computation """

    r = requests.get(url=PROMETHEUS_URL + '/api/v1/query', params=PROM_PARAMS)
    data = r.json()
    prom_df = sanitize_prometheus_response(data)
    # print(prom_df.head())


    es_json_params = json.dumps(ES_PARAMS)
    r = requests.get(ELASTIC_QUERY_URL, headers=HEADERS, auth=('n6saha', 'password'), data=es_json_params,  verify=False)
    data = r.json()
    es_df = sanitize_elastic_response(data)
    # print(es_df.head())

    # merge should get rid of old ES entries
    # since prom should only be collecting information about active series
    merged_df = prom_df.merge(es_df, on=["n3_ipaddr", "seid", "pdrid"])
    merged_df = merged_df.drop_duplicates() 
    # print(merged_df.head())
    return merged_df

def get_slice_throughput(df):
    result = df.groupby(["snssai", "direction"])["value"].sum()
    print(result)  # prints dataframe

def get_slice_x1_throughput_downlink(df):
    """ 
    get slice throughput from slice with SNSSAI 1@010203 on downlink
    used to compare with iperf test
    """
    mask = (df["snssai"] == "1@010203") & (df["direction"] == "downlink")
    result = df[mask]["value"].sum()
    result_mbits = (float(result) * 8) / (10 ** 6)
    print("{} Mbits/sec".format(result_mbits))

def get_slice_x1_throughput_uplink(df):
    """ 
    get slice throughput from slice with SNSSAI 1@010203 on uplink
    used to compare with iperf test
    """
    mask = (df["snssai"] == "1@010203") & (df["direction"] == "uplink")
    result = df[mask]["value"].sum()
    result_mbits = (float(result) * 8) / (10 ** 6)
    print("{} Mbits/sec".format(result_mbits))

    


def get_per_session_throughput(df):
    """ get slice throughput per PDU session """
    result = df.groupby(["snssai", "direction", "seid"])["value"].sum()
    print(result)  # prints dataframe



def run_kpi_computation():
    df = send_queries()

    print("Per slice throughput:")
    get_slice_throughput(df)

    print("\n\n")

    print("Per PDU session throughput:")
    get_per_session_throughput(df)


if __name__ == "__main__":

    run_kpi_computation()
    


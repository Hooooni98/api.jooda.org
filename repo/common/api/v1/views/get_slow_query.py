from django.http import JsonResponse
import requests
import logging
import csv


def get_slow_query(request):
    baseURL = "http://localhost:8000/api/v1/"
    logger = logging.getLogger("django.db.backends")

    get_administrator_query(baseURL, logger)

    write_report()
    return JsonResponse({"status": "available"})


def get_administrator_query(baseURL, logger):
    headers = {"Authorization": "test_church"}

    def call_api(url):
        logger.debug(f"-{url}")
        requests.get(f"{baseURL}{url}", headers=headers)

    call_api("administrators/churchs/info/")
    call_api("administrators/churchs/pastor/")
    call_api("administrators/churchs/history/")
    call_api("administrators/churchs/notice/")
    call_api("administrators/churchs/weekly/")
    call_api("administrators/churchs/member/")
    call_api("administrators/churchs/calendar/")


def write_report():
    def get_api_total_time(reports):
        result = []
        total_time = 0
        for report in reports:
            if len(report) == 1:
                result.append(total_time)
                total_time = 0
            else:
                total_time += float(report[0])
        result.append(total_time)
        return result

    reports = []
    results = []
    with open("slow_query.csv") as slow_query:
        for line in slow_query:
            if line[0] == "(" or line[0] == "-":
                index = line.find(")", 0, 10)
                if index == -1:
                    reports.append([line[1:-2]])
                else:
                    time = line[: index + 1][1:-1]
                    reports.append([time, line[index + 1 :]])

    api_total_time = get_api_total_time(reports)
    time_index = 1
    for report in reports:
        if len(report) == 1:
            results.append(
                [report[0], "Total Time : " + str(api_total_time[time_index])[:6]]
            )
            time_index += 1
        elif len(report) == 2 and len(report[1]) > 5:
            results.append([report[0], report[1]])

    file = "slow_query_report.csv"

    w = open(f"{file}", "w", encoding="utf-8")
    wr = csv.writer(w)

    wr.writerow(["Time", "QueryContent"])

    for result in results:
        wr.writerow([result[0], result[1]])
    w.close()

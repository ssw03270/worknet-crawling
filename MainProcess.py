# encoding='utf-8-sig'

from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import urllib.request
import time


# Scroll the entered url(=html) to the bottom and return the source.
def get_scrolled_html(urlList):
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    soupList = []
    for url in urlList:
        driver.get(url)
        html_source = driver.page_source
        soupList.append(BeautifulSoup(html_source, "html.parser"))
    driver.quit()
    return soupList

def get_data(soup):
    # soup has each page's html


    titleList = []      # 업무 이름
    payList = []        # 임금
    taskList = []       # 담당 업무
    timeList1 = []      # 업무 날짜
    timeList2 = []      # 업무 시간
    detailList = []     # 조건, 학력, 지역
    urlList = []        # 세부링크

    dataList = []       # 모든 데이타 총합
    for content in range(1, 11):
        try:
            tdList =  soup.find('tr', {'id': 'list' + str(content)}).find_all('td')
            titleList.append(tdList[2].find('div', {'class': 'cp-info-in'}).find('a').text.strip())

            imsiPay = tdList[3].find('div', {'class': 'cp-info'}).find('p').text.split()
            payList.append(str(imsiPay[0] + ' | ' + imsiPay[1] + imsiPay[2] + ' ' + imsiPay[3]))
            try:
                payList[content - 1] += ' ' + imsiPay[4] + imsiPay[5]
            except:
                print("error")
            pList1 = tdList[3].find('div', {'class': 'cp-info'}).find_all('p')
            imsiTime1 = pList1[2].text.split()
            timeList1.append(str(imsiTime1[0] + ' | ' + imsiTime1[1]))
            timeList2.append(str(pList1[3].text.strip()))

            taskList.append(soup.find('tr', {'id': 'list' + str(content)}).find('p', {'id': 'jobContLine' + str(content)}).text.strip())

            pList2 = tdList[2].find('div', {'class': 'cp-info'}).find_all('p')
            imsiDetail = pList2[2].text.split()
            detailList.append(str(imsiDetail[0] + ' | ' + imsiDetail[1] + ' | ' + imsiDetail[2] + ' ' + imsiDetail[3] + ' ' + imsiDetail[4]))

            urlList.append("https://www.work.go.kr" + tdList[2].find('div', {'class': 'cp-info-in'}).find('a')["href"])

            currentLine = content - 1
            dataList.append([titleList[currentLine], payList[currentLine], timeList1[currentLine], timeList2[currentLine], taskList[currentLine], detailList[currentLine], urlList[currentLine]])


        except:
            print("error")
    return dataList

def max_page_num(soup):
    return len(soup.find('div', {'class': 'nav_wrp'}).find_all('a'))

if __name__ == "__main__":
    age = "B"                               # 장년
    region = ''             # 지역
    holiday = ''            # 근무일
    pay = ''                # 급여
    minPay = ''
    maxPay = ''

    for occupation in range(1, 14):
        occupationTitle = ''
        fR = open('input.csv', 'r', encoding='utf-8-sig', newline='\n')
        rdr = csv.reader(fR)
        for line in rdr:
            if line[0] == str(occupation):
                occupationTitle = line[1]
                break
        occupation = '0' + str(occupation)
        urlFirst = [
            'https://www.work.go.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do?careerTo=&keywordJobCd=&occupation=' + occupation + '&rot2WorkYn=&templateInfo=&payGbn=' + pay + '&resultCnt=10&keywordJobCont=&cert=&cloDateStdt=&moreCon=more&minPay=' + minPay + '&codeDepth2Info=11000&isChkLocCall=&sortFieldInfo=DATE&major=&resrDutyExcYn=&sortField=DATE&staArea=&sortOrderBy=DESC&keyword=&termSearchGbn=all&benefitSrchAndOr=O&disableEmpHopeGbn=&webIsOut=&actServExcYn=&keywordStaAreaNm=&maxPay=' + maxPay + '&emailApplyYn=&listCookieInfo=DTL&pageCode=&codeDepth1Info=11000&keywordEtcYn=&publDutyExcYn=&keywordJobCdSeqNo=&exJobsCd=&templateDepthNmInfo=&computerPreferential=&regDateStdt=&employGbn=&empTpGbcd=&region=' + region + '&resultCntInfo=10&siteClcd=all&cloDateEndt=&sortOrderByInfo=DESC&currntPageNo=1&indArea=&careerTypes=&searchOn=Y&subEmpHopeYn=&academicGbn=&foriegn=&templateDepthNoInfo=&mealOfferClcd=&station=&moerButtonYn=Y&holidayGbn=' + holiday + '&enterPriseGbn=all&academicGbnoEdu=noEdu&cloTermSearchGbn=all&keywordWantedTitle=&stationNm=&benefitGbn=&keywordFlag=&essCertChk=&isEmptyHeader=&depth2SelCode=&_csrf=148b0b8e-5551-4671-aee9-ac652824f09d&keywordBusiNm=&preferentialGbn=' + age + '&rot3WorkYn=&pfMatterPreferential=&regDateEndt=&staAreaLineInfo1=11000&staAreaLineInfo2=1&pageIndex=1&termContractMmcnt=&careerFrom=&laborHrShortYn=#viewSPL']
        maxPage = max_page_num(get_scrolled_html(urlFirst)[0]) + 1

        urlList = []
        for page in range(1, maxPage):
            url = 'https://www.work.go.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do?careerTo=&keywordJobCd=&occupation=' + occupation + '&rot2WorkYn=&templateInfo=&payGbn=' + pay + '&resultCnt=10&keywordJobCont=&cert=&cloDateStdt=&moreCon=more&minPay' + minPay + '=&codeDepth2Info=11000&isChkLocCall=&sortFieldInfo=DATE&major=&resrDutyExcYn=&sortField=DATE&staArea=&sortOrderBy=DESC&keyword=&termSearchGbn=all&benefitSrchAndOr=O&disableEmpHopeGbn=&webIsOut=&actServExcYn=&keywordStaAreaNm=&maxPay=' + maxPay + '&emailApplyYn=&listCookieInfo=DTL&pageCode=&codeDepth1Info=11000&keywordEtcYn=&publDutyExcYn=&keywordJobCdSeqNo=&exJobsCd=&templateDepthNmInfo=&computerPreferential=&regDateStdt=&employGbn=&empTpGbcd=&region=' + region + '&resultCntInfo=10&siteClcd=all&cloDateEndt=&sortOrderByInfo=DESC&currntPageNo=1&indArea=&careerTypes=&searchOn=Y&subEmpHopeYn=&academicGbn=&foriegn=&templateDepthNoInfo=&mealOfferClcd=&station=&moerButtonYn=Y&holidayGbn=' + holiday + '&enterPriseGbn=all&academicGbnoEdu=noEdu&cloTermSearchGbn=all&keywordWantedTitle=&stationNm=&benefitGbn=&keywordFlag=&essCertChk=&isEmptyHeader=&depth2SelCode=&_csrf=148b0b8e-5551-4671-aee9-ac652824f09d&keywordBusiNm=&preferentialGbn=' + age + '&rot3WorkYn=&pfMatterPreferential=&regDateEndt=&staAreaLineInfo1=11000&staAreaLineInfo2=1&pageIndex=' + str(
                page) + '&termContractMmcnt=&careerFrom=&laborHrShortYn=#viewSPL'
            urlList.append(url)
        soupList = get_scrolled_html(urlList)

        fileTitle = occupationTitle + '.csv'
        fW = open(fileTitle, 'w', encoding='utf-8-sig', newline='\n')
        wr = csv.writer(fW)
        for soup in soupList:
            dataList = (get_data(soup))
            for data in dataList:
                wr.writerow(data)
        fW.close()




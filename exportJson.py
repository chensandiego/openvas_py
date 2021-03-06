import gvm 
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeTransform 
from gvm.xml import pretty_print
import xml.etree.ElementTree as ET
import untangle
import base64
import csv, json

 
 

def exportReports():
    '''
     This will add a target to the list and start the sca of the targets
    '''
    connection = gvm.connections.TLSConnection(hostname='localhost')
    transform =EtreeTransform() 
    with Gmp(connection,transform=transform) as gmp:
        gmp.authenticate('admin', 'admin')  

        #Get the CSV report type
        reportFormatID=""
        report_format = gmp.get_report_formats()
        report_root = ET.fromstring(report_format)
        for report in report_root:
            report.tag == "report_format"
            for report_format in report:
                if report_format.text == 'CSV result list.':
                    reportFormatID= report.attrib.get('id')
                    #reportFromatData = gmp.get_report_format(reportFormatID)
                    #pretty_print(reportFromatData)

        getReports=[]
        allreports = gmp.get_reports()
        allreports_root = ET.fromstring(allreports)
        for report in allreports_root:
            if report.tag == 'report':
                for onereport in report:
                    if onereport.tag =='report':
                        pretty_print(onereport)
                        print(report.attrib)
                        getReports.append(report.attrib.get('id'))


        #Get out the reports and get them as csv files to use
        for reportID in getReports:
            print("################{0}".format(reportID))
            reportscv = gmp.get_report(reportID,report_format_id=reportFormatID,filter="apply_overrides=0 min_qod=70",ignore_pagination=True,details=True)
            #pretty_print(reportscv)
            obj = untangle.parse(reportscv)
            resultID = obj.get_reports_response.report['id']
            base64CVSData = obj.get_reports_response.report.cdata
            data = str(base64.b64decode(base64CVSData),"utf-8")
            #print(data)

            #Write the result to file
            writeResultToFile(resultID,data)
            

       #for reports in reportrow.iter('report'):
            #    print(ET.tostring(reports,method='text', encoding='utf8').decode('utf8'))

        
def writeResultToFile(name,data):
    '''
    This will write the data into a file
    '''

    csvFilePath = "report.csv"
    jsonFilePath = "report.json"

    f = open(csvFilePath, "w")
    f.write(data)
    f.close()



    #read the csv and add the data to a dictionary

    jsonFile = open(jsonFilePath, "w")
    with open (csvFilePath) as csvFile:
        csvReader = csv.DictReader(csvFile)
        for csvRow in csvReader:
            jsonFile.write(json.dumps(csvRow)+"\n")
    jsonFile.close()
    csvFile.close()


if __name__=="__main__":
    exportReports() 
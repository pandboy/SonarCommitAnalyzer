import subprocess
import urllib.request
import zipfile
import shutil
import os
import utils

url_sonar_scanner = "https://sonarsource.bintray.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-3.0.3.778-windows.zip"
sonar_scanner_zip = "C:/Sonar/sonar-scanner.zip"

utils.print_(">> Configuring First Run ...")

directory = "C:/Sonar"
os.makedirs(directory, exist_ok=True)
if not os.path.exists("C:/Sonar/sonar-scanner"):
    if not os.path.exists(sonar_scanner_zip):
        utils.print_(">> Downloading Sonar Scanner ...")
        urllib.request.urlretrieve(url_sonar_scanner, sonar_scanner_zip)    

if os.path.exists(sonar_scanner_zip):
    with zipfile.ZipFile(sonar_scanner_zip, "r") as zipfile:
        zipfile.extractall("C:/Sonar")
    os.remove(sonar_scanner_zip)

if os.path.exists("C:/Sonar/sonar-scanner-3.0.3.778-windows"):
    os.rename("C:/Sonar/sonar-scanner-3.0.3.778-windows", "C:/Sonar/sonar-scanner")

directory = "C:/Sonar/issues-report"
os.makedirs(directory, exist_ok=True)

file = "C:/Sonar/template/template.sonarsource.properties"
os.makedirs(os.path.dirname(file), exist_ok=True)

with open(file, "w") as f:
    f.writelines("sonar.host.url={url}\n"\
        "sonar.login={login}\n"\
        "sonar.password={password}\n"\
        "\n"\
        "sonar.projectBaseDir={repository}\n"\
        "sonar.projectKey={system}\n"\
        "sonar.projectName={system}\n"\
        "sonar.projectVersion={branch}\n"\
        "{sources}\n"\
        "sonar.language={language}\n"\
        "\n"\
        "sonar.analysis.mode=preview\n"\
        "\n"\
        "sonar.issuesReport.html.enable=true\n"\
        "sonar.issuesReport.html.location=C:/Sonar/issues-report/{system}/\n"\
        "sonar.issuesReport.html.name=issues-report-{system}\n"\
        "sonar.issuesReport.console.enable=true\n"\
        "\n"\
        "{modules}")

utils.ok_text("Directories created.")

utils.print_(">> Instal GitPython ...")

output = subprocess.run("pip install GitPython", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, encoding="utf-8")

utils.print_(output.stdout)

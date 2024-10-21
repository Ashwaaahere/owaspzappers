from django.shortcuts import render, redirect
import os
import subprocess
import urllib.parse  # For URL encoding and decoding

def index(request):
    if request.method == "POST":
        link = request.POST.get("link")
        print(link)

        # URL encode the link to ensure it passes safely as a parameter
        encoded_link = urllib.parse.quote(link, safe='')

        # Redirect to the report view with the encoded link
        return redirect("report", link=encoded_link)
    return render(request, "index.html")


def report(request, link):
    # Decode the link to get the original URL
    decoded_link = urllib.parse.unquote(link)

    def run_wapiti(target_url):
        try:
            os.environ['PYTHONIOENCODING'] = 'utf-8'
            result = subprocess.run(
                ['wapiti', '-u', target_url, '--format', 'json', '-o', 'wapiti_report.json'],  # Fix the output format
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )

            if result.returncode != 0:
                print(f"Error running Wapiti: {result.stderr}")
            else:
                print("Wapiti scan completed successfully.")
                print(f"Output: {result.stdout}")
                
                

                with open('wapiti_report.json', 'r', encoding='utf-8') as report_file:
                    wapiti_results = report_file.read()
                    print(f"Wapiti Report:\n{wapiti_results}")
                    data=wapiti_results
                    return data
        except Exception as e:
            print(f"An error occurred: {e}")

    # Run the Wapiti scan on the decoded link
    data=run_wapiti(decoded_link)

    return render(request, "report.html", {"text": data})

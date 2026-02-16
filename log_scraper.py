import re
import csv
import time
from google import genai

# --- CONFIGURATION ---
# PASTE YOUR KEY HERE INSIDE THE QUOTES
API_KEY = "YOUR_API_KEY_HERE"

# Setup the Client
client = genai.Client(api_key=API_KEY)

# Use the model that worked for you before
model_name = "gemini-2.0-flash"

log_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) ERROR (.*)"

print("--- 🤖 AI LOG AUDITOR STARTING  ---")
print("--- ⏳ SCANNING LOGS... ---")

# Open a new CSV file to save the report
with open("error_report_ai.csv", "w", newline="", encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Error Message", "AI Explanation"])

    try:
        with open("server.log", "r", encoding='utf-8') as log_file:
            for line in log_file:
                match = re.search(log_pattern, line)
                if match:
                    timestamp = match.group(1)
                    message = match.group(2)
                    print(f"⚠️ Found Error: {message}")

                    explanation = "AI Explanation Unavailable"

                    # --- THE AI MAGIC ---
                    try:
                        # Check if it's a real key (longer than 20 chars)
                        if len(API_KEY) > 20:
                            print("   ... Asking AI for help ...")
                            response = client.models.generate_content(
                                model=model_name,
                                contents=f"Explain this server error in 1 short sentence: {message}"
                            )
                            explanation = response.text
                            print(f"   🤖 AI Says: {explanation}")
                        else:
                            print("   ℹ️ Skipped AI (Placeholder key detected)")

                    except Exception as e:
                        explanation = f"AI Error: {str(e)}"
                        print(f"   ⏳ Could not get AI response: {e}")

                    # Write to CSV
                    writer.writerow([timestamp, message, explanation])

                    # --- THE SECRET SAUCE ---
                    # We wait 30 seconds to force a reset of the Rate Limit
                    print("    ⏳ Cooldown: Waiting 30s to satisfy Google Free Tier...")
                    time.sleep(30)

        print("--- 🏁 REPORT GENERATED: error_report_ai.csv ---")
        print("--- ✅ DONE. Ready for Github! ---")

    except FileNotFoundError:
        print("❌ Error: 'server.log' file not found. Please create it first.")
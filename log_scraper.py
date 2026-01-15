import re # "Regular Expressions module"
import csv # New library for Excel files
import time # <--- NEW IMPORT
from google import genai # <--- NEW LIBRARY

# --- CONFIGURATION ---
# PASTE YOUR KEY HERE INSIDE THE QUOTES
# API_KEY = "AIzaSyDO9AhetPZEWOnPyYX6vGTTGCuJC9OpClw"
API_KEY = "YOUR_API_KEY_HERE"

# Setup the New AI Client
client = genai.Client(api_key=API_KEY)

# We use the model that we confirmed works for you
model_name = "gemini-2.0-flash"

# 1 . Define the Pattern we are looking for
# \d means "Digit" (number)
# {4} means "4 times" (like 2026)
# (.*)

log_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) ERROR (.*)"

print("--- 🤖 AI LOG AUDITOR STARTING  ---")
print("--- ⏳ SCANNING LOGS... ---")

# Open a new CSV file to save the report
with open("error_report_ai.csv", "w", newline="") as file:
    writer = csv.writer(file)
    # Write the Header row first
    writer.writerow(["Timestamp", "Error Message", "AI Explanation"]) # New Column!


# Read the log file
    try:
        with open("server.log", "r") as log_file:

            for line in log_file:
                # Check if the line matches our specific "ERROR" pattern 
                match = re.search(log_pattern, line) 

                if match:
                    #Group 1 is the Timestamp (from the first brackets)
                    timestamp = match.group(1)      

                    #Group 2 is the Message (from the second brackets)
                    message = match.group(2)  

                    print(f"⚠️ Found Error: {message}")
                    
                    # Default message if AI fails 
                    explanation = "AI Explanation Unavailable (Check API key)"

                    # --- THE AI MAGIC
                    try:
                        # Attempt to ask AI
                        # We send the error to Gemini
                        # NEW CODE: This uses the new Client syntax
                        # Only try if we have a real key (length check is a simple way to verify)
                        if len(API_KEY) > 20:
                            print("   ... Asking AI for help ...")
                            response = client.models.generate_content(
                                model = model_name,
                                contents = f"Explain this server error in 1 short sentence and suggest a fix: {message}"
                        )
                            explanation = response.text
                            print(f"  🤖 AI Says: {explanation}")
                        else:
                            print("  ℹ️ Skipped AI (Placeholder key detected)") 

                    except Exception as e:
                        # Graceful Error Handling 
                        explanation =  f"AI Error: {str(e)}"
                        print(f"    ⏳ COuld not get AI response: {e}")

                    # Write to the CSV file
                    # Save Timestamp, Error, AND the AI's Advice
                    writer.writerow([timestamp, message, explanation])
                    print("") # Empty Line for neatness

                    # Small pause to avoid hitting rate limits
                    time.sleep(1)

        print("--- 🏁 REPORT GENERATED: error_report.csv ---")
        print("--- ✅ DONE. Ready for Github! ---")

    except FileNotFoundError:    
        print("❌ Error: 'server.log' file not found. Please create it first.")
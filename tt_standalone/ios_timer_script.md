I currently run the following shortcut on my mac to allow me to capture time into a note. i want to do something similar in the terminal with cli and have it create a new file for the week and create a .md file with similar information. can you write me a short script to capture the following. pressing the shortcut once creates the "start time" and then pressing it a second tim will end the timer. input usually looks like: "Current Task Timer Provide summary of hours and minutes spent on the following tasks as text only no formatting, run the prompt in instructions ——— Admin Emails and whatsapp Start time: 27 Oct 2025 at 13:11:56 until End Time: 27 Oct 2025 at 15:14:58 ——— Pastoral & Community Peter Funeral Start time: 27 Oct 2025 at 15:39:43 until End Time: 27 Oct 2025 at 16:32:56 ——— Sermon Reading Start time: 28 Oct 2025 at 10:52:18 until End Time: 28 Oct 2025 at 12:38:20 ——— Operations Kalender Start time: 28 Oct 2025 at 13:23:04 until End Time: 28 Oct 2025 at 14:38:06 ———"

.

GPT-4o mini

Here’s a simple Bash script that you can use in the terminal to create a time tracker similar to what you've described. This script will allow you to start and stop a timer, logging the start and end timestamps for each task into a Markdown file named based on the current week.

### Bash Script for Time Tracking

bash

Copy Code

`#!/bin/bash # File to store the weekly log WEEKLY_LOG="time_log_$(date +%Y-%m-%d).md" # Check if the last command was a start or an end if [ -e "$WEEKLY_LOG" ]; then     LAST_LINE=$(tail -n 1 "$WEEKLY_LOG") else     touch "$WEEKLY_LOG"     LAST_LINE="" fi # Function to log time log_time() {     TASK_NAME="$1"     START_TIME="$2"     END_TIME="$3"     echo -e "\n$TASK_NAME\nStart time: $START_TIME\nuntil\nEnd Time: $END_TIME" >> "$WEEKLY_LOG" } # Start timer if [[ "$LAST_LINE" != *"End Time:"* ]]; then     # If no end time is found, it's starting a new task     echo "Enter the task name:"     read TASK_NAME    START_TIME=$(date +"%d %b %Y at %H:%M:%S")     echo "Timer started for: $TASK_NAME"     echo "$TASK_NAME - Start time: $START_TIME" >> "$WEEKLY_LOG" else     # Stopping the timer     END_TIME=$(date +"%d %b %Y at %H:%M:%S")     echo "Timer stopped."     log_time "$TASK_NAME" "$START_TIME" "$END_TIME" fi`

### Usage Instructions

1. **Create the Script:**
    
    - Open your terminal and create a new file:
        
        bash
        
        Copy Code
        
        `nano time_tracker.sh`
        
2. **Copy and Paste the Script:**
    
    - Paste the provided script into the editor and save the file (Ctrl + X, then Y, then Enter).
3. **Make the Script Executable:**
    
    - Run the following command to make your script executable:
        
        bash
        
        Copy Code
        
        `chmod +x time_tracker.sh`
        
4. **Run the Script:**
    
    - You can run the script with the following command:
        
        bash
        
        Copy Code
        
        `./time_tracker.sh`
        
5. **Logging Tasks:**
    
    - The first time you run the script, it will ask for the task name and will log the start time. Running it again will log the end time.

### Notes

- The script will create a Markdown file titled `time_log_YYYY-MM-DD.md` based on the current date.
- Each task's start and end time will log in the specified format.
- Adjust the date format in the `date` commands if you want a different format.

Feel free to modify the script as needed for your workflow!
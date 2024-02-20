from flask import Flask, render_template, redirect, url_for
import time


app = Flask(__name__)

# all in seconds for simplicity
LONG_BREAK = 15 * 60
SHORT_BREAK = 5 * 60
WORK_SESSION = 25 * 60

timer_duration = WORK_SESSION
timer_start_time = None
remaining_time = timer_duration  # Store remaining time when paused

def format_timer(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f'{minutes:02d}m {seconds:02d}s'

@app.route('/')
def index():
    global timer_start_time, remaining_time
    if timer_start_time:
        elapsed_time = time.time() - timer_start_time
        remaining_time -= int(elapsed_time)
        if remaining_time <= 0:
            timer_start_time = None
            remaining_time = timer_duration
            return render_template('index.html', timer=format_timer(0))
    return render_template('index.html', timer=format_timer(remaining_time))

@app.route('/start', methods=['POST'])
def start_timer():
    global timer_start_time, remaining_time
    if not timer_start_time:
        timer_start_time = time.time()
        remaining_time = timer_duration
    return redirect(url_for('index'))

@app.route('/pause', methods=['POST'])
def pause_timer():
    global timer_start_time, remaining_time
    if timer_start_time:
        elapsed_time = time.time() - timer_start_time
        remaining_time -= int(elapsed_time)
        timer_start_time = None
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset_timer():
    global timer_start_time, remaining_time
    timer_start_time = None
    remaining_time = timer_duration
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

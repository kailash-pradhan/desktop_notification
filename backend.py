import mysql.connector
from plyer import notification
from datetime import datetime
import time

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="notifications"
)


def is_valid_datetime(dt_str):
    try:
        datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False

# function to delete notification from database
def delete_notification(id):
    cursor = mydb.cursor()
    sql = "DELETE FROM notifications WHERE id = %s"
    cursor.execute(sql, (id,))
    mydb.commit()
    cursor.close()

# function to get next notification from database
def get_next_notification():
    cursor = mydb.cursor()
    sql = "SELECT id, title, description, TIMESTAMPDIFF(SECOND, NOW(), datetime) AS time_diff_seconds FROM notifications WHERE datetime >= NOW() ORDER BY datetime LIMIT 1"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result is not None:
        time_diff_seconds = int(result[3])
        time.sleep(time_diff_seconds)
    cursor.close()
    return result

while True:
    # get next notification from database
    notification_data = get_next_notification()

    # check if there is a notification to show
    if notification_data is not None:
        # show notification
        id, title, message, datetime_str = notification_data
        notification.notify(
            title=title,
            message=message,
            app_name="Notifier",
            app_icon="ico.ico",
            toast=True,
            timeout=10
        )

        # delete notification from database
        delete_notification(id)
    else:
        # sleep for a second if there are no notifications to show
        time.sleep(1)

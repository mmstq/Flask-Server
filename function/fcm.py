from pyfcm import FCMNotification

class FCM:
    def __init__(self):
        print("FCM init")
        api_key = "AAAAK2ZQLHk:APA91bGD8VFaq-WI7s2qdfr4C7r0isQ6Mr4T3UUmd4IaGsCuYk-Tze1neL00r7EkafJGTBmJ3nYw8G5YM64AsRaKvKFijqGLNMs680FjgVZaZ7pIQzakQCFgsvgnKyf5SP1ezxdjai6MZR-9hpcy83giSHFjFt7JtQ"
        self.push_service = FCMNotification(api_key=api_key)


    def send(self, title, body, data, topic):
        result = self.push_service.notify_topic_subscribers(
            topic_name=topic, message_body=body, message_title=title, data_message=data,
        )
        return result

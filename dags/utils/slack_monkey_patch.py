import airflow

from airflow.contrib.hooks.slack_webhook_hook import SlackWebhookHook


def apply_monkey_patch_if_needed():
    """
    Applies a monkey-patch to avoid a bug in Airflow 1.10.3.
    https://issues.apache.org/jira/browse/AIRFLOW-4262
    """
    if airflow.__version__ != '1.10.3':
        return

    def slack_webhook_hook_init(self, http_conn_id=None, webhook_token=None, message="", attachments=None, channel=None,
                                username=None, icon_emoji=None, link_names=False, proxy=None, *args, **kwargs):
        super(SlackWebhookHook, self).__init__(http_conn_id=http_conn_id, *args, **kwargs)
        self.webhook_token = self._get_token(webhook_token, http_conn_id)
        self.message = message
        self.attachments = attachments
        self.channel = channel
        self.username = username
        self.icon_emoji = icon_emoji
        self.link_names = link_names
        self.proxy = proxy

    SlackWebhookHook.__init__ = slack_webhook_hook_init

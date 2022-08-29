from app import celery
from app.lib.bukkit.info import BukkitServerInfo
from app.lib.clarence.metric import Metric
from app.lib.clarence.counter import MetricCounter

syncer = {
    "api": ["api_requests"],
    "plzmjoins": ["server_join"]
}


@celery.task(name="clarence.sync_counters")
def sync_counters():
    for metric_name, counter_list in syncer.items():
        metric = Metric(metric_name)
        for counter_name in counter_list:
            count = MetricCounter(counter_name)
            metric.sync_counter(count)

    return "Ok"


@celery.task(name="clarence.third_minute")
def third_minute():
    # Обновление данных по аккаунтам
    account_metrics = Metric("accounts_total")
    last_save_account_count = account_metrics.today().last_value
    current_account_count = BukkitServerInfo().get_account_count(update_cache=True)
    if last_save_account_count == 0:
        last_save_account_count = current_account_count
    new_accounts = current_account_count - last_save_account_count
    account_metrics.today().set(BukkitServerInfo().get_account_count(update_cache=True))
    new_account_metrics = Metric("accounts_new")
    new_account_metrics.today().set(new_accounts)
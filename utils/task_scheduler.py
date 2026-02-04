def start_background_tasks(scheduler, app):
    def job_with_context():
        with app.app_context():
            from utils.check_expired_file import search_expired_files_and_delete

            search_expired_files_and_delete()

    scheduler.add_job(
        id="delete_files",
        func=job_with_context,
        trigger="interval",
        minutes=1,
    )
    scheduler.start()

if __name__ == '__main__':

    from flask_script import Manager
    from flask_migrate import Migrate, MigrateCommand

    from app.app import create_app
    from app.models import db, User, Category, News

    app = create_app()

    migrate = Migrate(app, db)
    manager = Manager(app)

    manager.add_command('db', MigrateCommand)

    @manager.command
    def seed():
        # user
        u = User('prk', 'prk')

        db.session.add(u)

        # category
        categories = [
            Category('Important', 1),
            Category('More Important', 2),
            Category('Most Important', 3)
        ]
        for category in categories:
            db.session.add(category)

            # news
            for i in range(1, 3+1):
                news = News(category.name + ' News ' + str(i), 'Content here', category.id)

                db.session.add(news)

        db.session.commit()

    manager.run()

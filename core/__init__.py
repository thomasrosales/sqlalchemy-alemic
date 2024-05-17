from environs import Env

env = Env()

env.read_env()  # read .env file, if it exists

DATABASE_USERNAME = env.str("DB_USER", "root")
DATABASE_PASSWORD = env.str("DB_USER", "root")
DATABASE_HOST = env.str("DB_HOST", "localhost")
DATABASE_PORT = env.str("DB_PORT", "5432")
DATABASE_NAME = env.str("DB_NAME", "db")

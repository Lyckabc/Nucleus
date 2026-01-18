import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

def create_database_and_user():
    # 환경 변수 로드 (Docker Compose에서 주입)
    admin_user = os.getenv('DB_ADMIN_USER', 'postgres')
    admin_password = os.getenv('DB_ADMIN_PASSWORD')
    host = os.getenv('DB_HOST', 'DB_ADMIN_HOST')
    port = os.getenv('DB_PORT', 'DB_ADMIN_PORT')
    
    new_db = os.getenv('NEW_DB_NAME')
    new_user = os.getenv('NEW_DB_USER')
    new_pass = os.path.expandvars(os.getenv('NEW_DB_PASSWORD'))

    try:
        # 1. 관리자(postgres) DB에 연결
        conn = psycopg2.connect(
            dbname='postgres',
            user=admin_user,
            password=admin_password,
            host=host,
            port=port
        )
        conn.autocommit = True # DB 생성 시 트랜잭션 방지 설정
        cur = conn.cursor()

        # 2. 사용자(User) 생성 및 Superuser 권한 부여
        print(f"Checking if user '{new_user}' exists...")
        cur.execute(sql.SQL("SELECT 1 FROM pg_roles WHERE rolname = %s"), [new_user])
        if not cur.fetchone():
            cur.execute(sql.SQL("CREATE USER {} WITH SUPERUSER PASSWORD %s")
                        .format(sql.Identifier(new_user)), [new_pass])
            print(f"User '{new_user}' created with Superuser privileges.")
        else:
            print(f"User '{new_user}' already exists.")

        # 3. 데이터베이스(Database) 생성
        print(f"Checking if database '{new_db}' exists...")
        cur.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [new_db])
        if not cur.fetchone():
            cur.execute(sql.SQL("CREATE DATABASE {} OWNER {}")
                        .format(sql.Identifier(new_db), sql.Identifier(new_user)))
            print(f"Database '{new_db}' created successfully.")
        else:
            print(f"Database '{new_db}' already exists.")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_database_and_user()
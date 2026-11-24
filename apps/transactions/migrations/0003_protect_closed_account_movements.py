from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_account_is_closed"),
        ("transactions", "0002_alter_transaction_options"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE FUNCTION protect_closed_account_movements() RETURNS trigger
                LANGUAGE plpgsql AS $$
                DECLARE
                    previous_account bigint;
                    next_account bigint;
                    closed boolean;
                BEGIN
                    IF TG_OP <> 'INSERT' THEN
                        previous_account := OLD.account_id;
                    END IF;
                    IF TG_OP <> 'DELETE' THEN
                        next_account := NEW.account_id;
                    END IF;
                    FOR closed IN
                        SELECT is_closed FROM accounts_account
                        WHERE id IN (previous_account, next_account)
                        ORDER BY id FOR UPDATE
                    LOOP
                        IF closed THEN
                            RAISE EXCEPTION 'La cuenta está cerrada.'
                                USING ERRCODE = '23514';
                        END IF;
                    END LOOP;
                    IF TG_OP = 'DELETE' THEN
                        RETURN OLD;
                    END IF;
                    RETURN NEW;
                END;
                $$;
                CREATE TRIGGER protect_closed_account_movements
                BEFORE INSERT OR UPDATE OR DELETE ON transactions_transaction
                FOR EACH ROW EXECUTE FUNCTION protect_closed_account_movements();
            """,
            reverse_sql="""
                DROP TRIGGER protect_closed_account_movements ON transactions_transaction;
                DROP FUNCTION protect_closed_account_movements();
            """,
        )
    ]

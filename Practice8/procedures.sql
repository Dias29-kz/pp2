-- procedures.sql

-- 1. Upsert procedure
-- Егер name бар болса, phone update жасайды
-- Әйтпесе жаңа user қосады
CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR,
    p_phone VARCHAR,
    p_surname VARCHAR DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts
        SET phone = p_phone,
            surname = COALESCE(p_surname, surname)
        WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, surname, phone)
        VALUES (p_name, p_surname, p_phone);
    END IF;
END;
$$;


-- 2. Bulk insert procedure with validation
-- name[] және phone[] массив қабылдайды
-- Телефон дұрыс болмаса invalid_contacts деген temp table-ға сақтайды
CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_names VARCHAR[],
    p_phones VARCHAR[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
    current_name VARCHAR;
    current_phone VARCHAR;
BEGIN
    -- Қате мәліметтерді сақтау үшін уақытша кесте
    CREATE TEMP TABLE IF NOT EXISTS invalid_contacts (
        name VARCHAR,
        phone VARCHAR,
        reason TEXT
    ) ON COMMIT PRESERVE ROWS;

    -- Бұрынғы мәндерді тазалау
    DELETE FROM invalid_contacts;

    -- Екі массивтің өлшемі бірдей ме, тексеру
    IF array_length(p_names, 1) IS DISTINCT FROM array_length(p_phones, 1) THEN
        RAISE EXCEPTION 'Names array and phones array must have the same length';
    END IF;

    -- Loop арқылы жүріп шығамыз
    FOR i IN 1..array_length(p_names, 1) LOOP
        current_name := p_names[i];
        current_phone := p_phones[i];

        -- Phone validation:
        -- +7XXXXXXXXXX немесе тек 11 цифр форматтарын қабылдаймыз
        IF current_phone ~ '^\+7[0-9]{10}$' OR current_phone ~ '^[0-9]{11}$' THEN
            IF EXISTS (SELECT 1 FROM contacts WHERE name = current_name) THEN
                UPDATE contacts
                SET phone = current_phone
                WHERE name = current_name;
            ELSE
                BEGIN
                    INSERT INTO contacts(name, phone)
                    VALUES (current_name, current_phone);
                EXCEPTION
                    WHEN unique_violation THEN
                        INSERT INTO invalid_contacts(name, phone, reason)
                        VALUES (current_name, current_phone, 'Duplicate phone or name');
                END;
            END IF;
        ELSE
            INSERT INTO invalid_contacts(name, phone, reason)
            VALUES (current_name, current_phone, 'Invalid phone format');
        END IF;
    END LOOP;
END;
$$;


-- 3. Delete procedure by username or phone
CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM contacts
    WHERE name = p_value
       OR phone = p_value;
END;
$$;
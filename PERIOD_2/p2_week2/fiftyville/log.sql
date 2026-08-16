-- Keep a log of any SQL queries you execute as you solve the mystery.
-- .table
-- .schema crime_scene_reports

SELECT * FROM crime_scene_reports       -- select *(all)
WHERE year = 2024
    AND month = 7
    AND day = 28
    AND street = "Humphrey Street";

SELECT * FROM interviews
WHERE year = 2024
    AND month = 7
    AND day = 28
    AND transcript LIKE "%bakery%";

-- according to Ruth statement, i need to check security footage from parking ten min after the incident

SELECT * FROM bakery_security_logs
WHERE year = 2024
AND month = 7
AND day = 28
AND hour = 10

-- got 9 license plate info of exitance

SELECT * FROM people p
WHERE license_plate IN (
    'R3G7486','13FNH73','5P2BI95','94KL13X','6P58WS2','4328GD8','G412CB7',
    'L93JTIZ','322W7JE','0NTHK55','1106N58','NRYN856','WD5M8I6', 'V47T75I'
  );


-- Check phone calls under 60 seconds to see who was in contact

SELECT *
FROM phone_calls pc
WHERE caller IN (
  '(725) 555-4692','(301) 555-4174','(771) 555-6667',
  '(829) 555-5269','(130) 555-0289','(286) 555-6063',
  '(389) 555-5198','(770) 555-1861','(499) 555-9472',
  '(994) 555-3373','(286) 555-0131','(367) 555-5533',
  '(027) 555-1068','(194) 555-5027'
)
AND duration < 60
AND year = 2024
AND month = 7
AND day = 28;

-- Got 5 people in the result, but I only need one

SELECT *
FROM people p
WHERE phone_number IN (
  '(130) 555-0289',
  '(499) 555-9472',
  '(367) 555-5533',
  '(286) 555-6063',
  '(770) 555-1861'
);


-- Combine two tables to see who made money withdrawals

SELECT * FROM bank_accounts AS b
JOIN atm_transactions AS a
  ON b.account_number = a.account_number
WHERE a.atm_location = 'Leggett Street'
  AND a.year = 2024
  AND a.month = 7
  AND a.day = 28;

-- After combining, 9 people were found: 8 withdrew money and 1 made a deposit. I will focus on the 8 who withdrew money.
-- Find all people who:
-- Were seen at the bakery at 10:00 AM on July 28
-- Made a short phone call
-- Withdrew money from the Leggett Street ATM

Flew out the next day (July 29)
SELECT DISTINCT p.* FROM people AS p
JOIN bakery_security_logs AS b
    ON p.license_plate = b.license_plate
JOIN phone_calls AS ph
    ON p.phone_number = ph.caller
JOIN bank_accounts AS ba
    ON p.id = ba.person_id
JOIN atm_transactions AS at
    ON ba.account_number = at.account_number
JOIN passengers AS pa
    ON p.passport_number = pa.passport_number
JOIN flights AS f
    ON pa.flight_id = f.id
WHERE b.year = 2024
  AND b.month = 7
  AND b.day = 28
  AND b.hour = 10
  AND ph.duration < 60
  AND ph.year = 2024
  AND ph.month = 7
  AND ph.day = 28
  AND at.year = 2024
  AND at.month = 7
  AND at.day = 28
  AND at.atm_location = 'Leggett Street'
  AND at.transaction_type = 'withdraw'
  AND f.year = 2024
  AND f.month = 7
  AND f.day = 29;

-- Found 3 people: 'Taylor', 'Diana', and 'Bruce'

SELECT * FROM bakery_security_logs bsl
WHERE license_plate  IN ('1106N58','322W7JE','94KL13X');


-- Looking up flight information

SELECT * FROM flights f
WHERE day = 29
AND year = 2024
AND month = 7


-- Checking the origin and destination airports

SELECT * FROM airports
WHERE id = 8

SELECT * FROM airports
WHERE id = 4

-- Suspect escaped to New York City
-- Trying to identify the thief with the information gathered

SELECT * FROM people AS p
JOIN passengers AS q
  ON p.passport_number = q.passport_number
WHERE p.license_plate IN (
  '1106N58',
  '322W7JE',
  '94KL13X'
);

-- Only 2 suspects remain: Taylor and Bruce
-- Matching license plate with bakery logs to determine the thief and timing

SELECT * FROM bakery_security_logs bsl
 WHERE bsl.license_plate IN ('1106N58','94KL13X')
 AND year = 2024
 AND month = 7
 AND day = 28;

-- Suspects left at 10:18 and 10:35; the 10:18 one matches the witness statement

SELECT * FROM people
WHERE license_plate  = '94KL13X'

-- Bruce is identified as the thief
-- Next, I will use Bruce’s phone number to find the accomplice in the phone records

SELECT * FROM phone_calls pc
WHERE caller = '(367) 555-5533'
AND year = 2024
AND month = 7
AND day = 28
AND duration < 60;

-- Found 1 person that matches our specifications
-- Checking the receiver’s phone number to identify the accomplice

SELECT * FROM people
WHERE phone_number = '(375) 555-8161'

-- Confirms Robin is the accomplice
-- Mystery solved: Bruce is the thief, and Robin is the accomplice.

-- The songs that feature other artists

SELECT name
FROM songs
WHERE name LIKE '%feat.%';      -- % cointains the command

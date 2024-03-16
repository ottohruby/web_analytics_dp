SELECT cron.unschedule_all();

SELECT cron.schedule('*/30 * * * * *', $$DO BEGIN PERFORM process_event_data(1); END$$);

SELECT cron.schedule('*/1 * * * *', $$DO BEGIN PERFORM process_event_data(1); END$$);
SELECT cron.schedule('2 */1 * * *', $$DO BEGIN PERFORM process_event_data(2); END$$);
SELECT cron.schedule('5 1 * * *', $$DO BEGIN PERFORM process_event_data(3); END$$);
SELECT cron.schedule('10 2 1 * *', $$DO BEGIN PERFORM process_event_data(4); END$$);

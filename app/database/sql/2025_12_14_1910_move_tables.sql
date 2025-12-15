-- Move tables from public to app
ALTER TABLE IF EXISTS public.roles SET SCHEMA app;
ALTER TABLE IF EXISTS public.users SET SCHEMA app;

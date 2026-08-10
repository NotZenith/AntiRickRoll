-- Projects Table
CREATE TABLE projects (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  thumbnail_url TEXT,
  github_url TEXT,
  live_url TEXT,
  technologies TEXT[],
  category TEXT,
  featured BOOLEAN DEFAULT false,
  "order" INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone(\'utc\'::text, now()) NOT NULL
);

-- Photography Table
CREATE TABLE photos (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  title TEXT,
  description TEXT,
  image_url TEXT NOT NULL,
  category TEXT,
  tags TEXT[],
  featured BOOLEAN DEFAULT false,
  "order" INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone(\'utc\'::text, now()) NOT NULL
);

-- Messages Table
CREATE TABLE messages (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  subject TEXT,
  message TEXT NOT NULL,
  read BOOLEAN DEFAULT false,
  archived BOOLEAN DEFAULT false,
  browser_info JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone(\'utc\'::text, now()) NOT NULL
);

-- Settings Table (for Homepage Content)
CREATE TABLE settings (
  id TEXT PRIMARY KEY,
  value JSONB NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone(\'utc\'::text, now()) NOT NULL
);

-- Enable RLS
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE photos ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE settings ENABLE ROW LEVEL SECURITY;

-- Policies for public reading
CREATE POLICY "Allow public read on projects" ON projects FOR SELECT USING (true);
CREATE POLICY "Allow public read on photos" ON photos FOR SELECT USING (true);
CREATE POLICY "Allow public insert on messages" ON messages FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public read on settings" ON settings FOR SELECT USING (true);

-- Policies for authenticated admin
CREATE POLICY "Allow admin all on projects" ON projects USING (auth.role() = \'authenticated\');
CREATE POLICY "Allow admin all on photos" ON photos USING (auth.role() = \'authenticated\');
CREATE POLICY "Allow admin all on messages" ON messages USING (auth.role() = \'authenticated\');
CREATE POLICY "Allow admin all on settings" ON settings USING (auth.role() = \'authenticated\');

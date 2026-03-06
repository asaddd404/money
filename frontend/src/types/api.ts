export type UserMe = {
  id: number;
  center_id: number;
  email: string;
  full_name: string;
  role: 'student' | 'teacher' | 'manager' | 'admin';
};

export type Group = {
  id: number;
  center_id: number;
  name: string;
  owner_teacher_id: number;
};

export type Product = {
  id: number;
  name: string;
  price: number;
  stock: number;
  is_active: boolean;
};

export type LeaderboardRow = {
  student_id: number;
  score: number;
  last_award: string | null;
};

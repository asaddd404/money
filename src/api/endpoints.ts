export const endpoints = {
  auth: {
    login: '/auth/login',
    refresh: '/auth/refresh',
    logout: '/auth/logout'
  },
  users: { me: '/users/me' },
  awards: '/awards',
  groups: '/groups',
  products: '/products',
  orders: '/orders',
  leaderboards: '/leaderboards',
  admin: {
    auditLogs: '/admin/audit-logs',
    teacherPolicies: '/admin/teacher-policies'
  }
} as const;

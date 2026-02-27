import { AnimatePresence, motion } from 'framer-motion';
import { Navigate, Route, Routes, useLocation } from 'react-router-dom';
import { AppShell } from '@/app/layouts/AppShell';
import { AuthLayout } from '@/app/layouts/AuthLayout';
import { LoginPage } from '@/features/auth/LoginPage';
import { RegisterPage } from '@/features/auth/RegisterPage';
import { GlobalErrorPage, NotFoundPage, ProfilePage, SettingsPage } from '@/features/common/pages';
import { StudentGroupsPage, StudentHomePage, StudentLeaderboardsPage, StudentOrdersPage, StudentShopPage, StudentTransactionsPage, StudentWalletPage } from '@/features/student/pages';
import { TeacherAwardPage, TeacherEnrollmentsPage, TeacherGroupsPage, TeacherHomePage, TeacherLeaderboardsPage } from '@/features/teacher/pages';
import { ManagerAuditPage, ManagerHomePage, ManagerOrdersPage, ManagerProductsPage } from '@/features/manager/pages';
import { AdminHomePage, AdminPoliciesPage } from '@/features/admin/pages';
import { useAuthStore } from '@/store/auth.store';

const ProtectedRoute = ({ roles, children }: { roles: string[]; children: JSX.Element }) => {
  const role = useAuthStore((s) => s.role);
  if (!role) return <Navigate to="/auth/login" replace />;
  if (!roles.includes(role)) return <Navigate to={`/app/${role}/home`} replace />;
  return children;
};

const AnimatedPage = ({ children }: { children: JSX.Element }) => (
  <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }} transition={{ duration: 0.2 }}>
    {children}
  </motion.div>
);

export const AppRouter = () => {
  const location = useLocation();
  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/auth" element={<AuthLayout />}>
          <Route path="login" element={<LoginPage />} />
          <Route path="register" element={<RegisterPage />} />
        </Route>

        <Route path="/app" element={<AppShell />}>
          <Route path="profile" element={<AnimatedPage><ProfilePage /></AnimatedPage>} />

          <Route path="student">
            <Route path="home" element={<ProtectedRoute roles={['student']}><AnimatedPage><StudentHomePage /></AnimatedPage></ProtectedRoute>} />
            <Route path="wallet" element={<ProtectedRoute roles={['student']}><AnimatedPage><StudentWalletPage /></AnimatedPage></ProtectedRoute>} />
            <Route path="transactions" element={<ProtectedRoute roles={['student']}><AnimatedPage><StudentTransactionsPage /></AnimatedPage></ProtectedRoute>} />
            <Route path="groups" element={<ProtectedRoute roles={['student']}><AnimatedPage><StudentGroupsPage /></AnimatedPage></ProtectedRoute>} />
            <Route path="shop" element={<ProtectedRoute roles={['student']}><AnimatedPage><StudentShopPage /></AnimatedPage></ProtectedRoute>} />
            <Route path="orders" element={<ProtectedRoute roles={['student']}><AnimatedPage><StudentOrdersPage /></AnimatedPage></ProtectedRoute>} />
            <Route path="leaderboards" element={<ProtectedRoute roles={['student']}><AnimatedPage><StudentLeaderboardsPage /></AnimatedPage></ProtectedRoute>} />
            <Route path="settings" element={<SettingsPage />} />
          </Route>

          <Route path="teacher">
            <Route path="home" element={<ProtectedRoute roles={['teacher', 'admin']}><AnimatedPage><TeacherHomePage /></AnimatedPage></ProtectedRoute>} />
            <Route path="groups" element={<ProtectedRoute roles={['teacher', 'admin']}><TeacherGroupsPage /></ProtectedRoute>} />
            <Route path="enrollments" element={<ProtectedRoute roles={['teacher', 'admin']}><TeacherEnrollmentsPage /></ProtectedRoute>} />
            <Route path="award" element={<ProtectedRoute roles={['teacher', 'admin']}><TeacherAwardPage /></ProtectedRoute>} />
            <Route path="leaderboards" element={<ProtectedRoute roles={['teacher', 'admin']}><TeacherLeaderboardsPage /></ProtectedRoute>} />
            <Route path="settings" element={<SettingsPage />} />
          </Route>

          <Route path="manager">
            <Route path="home" element={<ProtectedRoute roles={['manager', 'admin']}><ManagerHomePage /></ProtectedRoute>} />
            <Route path="products" element={<ProtectedRoute roles={['manager', 'admin']}><ManagerProductsPage /></ProtectedRoute>} />
            <Route path="orders" element={<ProtectedRoute roles={['manager', 'admin']}><ManagerOrdersPage /></ProtectedRoute>} />
            <Route path="audit" element={<ProtectedRoute roles={['manager', 'admin']}><ManagerAuditPage /></ProtectedRoute>} />
            <Route path="settings" element={<SettingsPage />} />
          </Route>

          <Route path="admin">
            <Route path="home" element={<ProtectedRoute roles={['admin']}><AdminHomePage /></ProtectedRoute>} />
            <Route path="products" element={<ProtectedRoute roles={['admin']}><ManagerProductsPage /></ProtectedRoute>} />
            <Route path="orders" element={<ProtectedRoute roles={['admin']}><ManagerOrdersPage /></ProtectedRoute>} />
            <Route path="policies" element={<ProtectedRoute roles={['admin']}><AdminPoliciesPage /></ProtectedRoute>} />
            <Route path="audit" element={<ProtectedRoute roles={['admin']}><ManagerAuditPage /></ProtectedRoute>} />
            <Route path="settings" element={<SettingsPage />} />
          </Route>
        </Route>

        <Route path="/" element={<Navigate to="/auth/login" replace />} />
        <Route path="/error" element={<GlobalErrorPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </AnimatePresence>
  );
};

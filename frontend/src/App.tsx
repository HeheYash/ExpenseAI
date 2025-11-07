import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { motion } from 'framer-motion'

import { useAuthStore } from '@store/authStore'
import { AppLayout } from '@components/layout/AppLayout'
import { AuthLayout } from '@components/layout/AuthLayout'

// Lazy load pages for better performance
const Dashboard = React.lazy(() => import('@pages/Dashboard'))
const Login = React.lazy(() => import('@pages/auth/Login'))
const Register = React.lazy(() => import('@pages/auth/Register'))
const Transactions = React.lazy(() => import('@pages/Transactions'))
const Categories = React.lazy(() => import('@pages/Categories'))
const Settings = React.lazy(() => import('@pages/Settings'))
const NotFound = React.lazy(() => import('@pages/NotFound'))

// Loading component for lazy loaded routes
const PageLoader = () => (
  <div className="flex items-center justify-center min-h-screen">
    <motion.div
      className="w-12 h-12 border-4 border-white/20 border-t-primary-500 rounded-full"
      animate={{ rotate: 360 }}
      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
    />
  </div>
)

// Protected route wrapper
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuthStore()

  if (isLoading) {
    return <PageLoader />
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}

// Public route wrapper (redirect if authenticated)
const PublicRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuthStore()

  if (isLoading) {
    return <PageLoader />
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />
  }

  return <>{children}</>
}

function App() {
  const { isLoading } = useAuthStore()

  // Show loading screen while checking authentication
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="text-center"
        >
          <motion.div
            className="w-16 h-16 border-4 border-white/20 border-t-primary-500 rounded-full mx-auto mb-4"
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          />
          <h1 className="text-2xl font-bold text-white mb-2">Expense Manager</h1>
          <p className="text-white/60">Loading your financial dashboard...</p>
        </motion.div>
      </div>
    )
  }

  return (
    <div className="App min-h-screen">
      <Routes>
        {/* Public routes */}
        <Route
          path="/login"
          element={
            <PublicRoute>
              <AuthLayout>
                <React.Suspense fallback={<PageLoader />}>
                  <Login />
                </React.Suspense>
              </AuthLayout>
            </PublicRoute>
          }
        />
        <Route
          path="/register"
          element={
            <PublicRoute>
              <AuthLayout>
                <React.Suspense fallback={<PageLoader />}>
                  <Register />
                </React.Suspense>
              </AuthLayout>
            </PublicRoute>
          }
        />

        {/* Protected routes */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <AppLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route
            path="dashboard"
            element={
              <React.Suspense fallback={<PageLoader />}>
                <Dashboard />
              </React.Suspense>
            }
          />
          <Route
            path="transactions"
            element={
              <React.Suspense fallback={<PageLoader />}>
                <Transactions />
              </React.Suspense>
            }
          />
          <Route
            path="categories"
            element={
              <React.Suspense fallback={<PageLoader />}>
                <Categories />
              </React.Suspense>
            }
          />
          <Route
            path="settings"
            element={
              <React.Suspense fallback={<PageLoader />}>
                <Settings />
              </React.Suspense>
            }
          />
        </Route>

        {/* 404 route */}
        <Route
          path="*"
          element={
            <React.Suspense fallback={<PageLoader />}>
              <NotFound />
            </React.Suspense>
          }
        />
      </Routes>
    </div>
  )
}

export default App
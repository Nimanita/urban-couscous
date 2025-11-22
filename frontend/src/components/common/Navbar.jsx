// src/components/common/Navbar.jsx
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { BookOpen, LayoutDashboard, LogOut, User, Menu, X } from 'lucide-react';
import { useState } from 'react';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [showDropdown, setShowDropdown] = useState(false);
  const [showMobileMenu, setShowMobileMenu] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const closeMobileMenu = () => {
    setShowMobileMenu(false);
  };

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="w-full px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/dashboard" className="flex items-center space-x-2">
              <div className="bg-primary-600 p-2 rounded-lg">
                <BookOpen className="h-6 w-6 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">
                Learning Tracker
              </span>
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden md:flex ml-10 space-x-4">
              <Link
                to="/dashboard"
                className="flex items-center space-x-1 px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-primary-600 hover:bg-primary-50"
              >
                <LayoutDashboard className="h-4 w-4" />
                <span>Dashboard</span>
              </Link>
              <Link
                to="/courses"
                className="flex items-center space-x-1 px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-primary-600 hover:bg-primary-50"
              >
                <BookOpen className="h-4 w-4" />
                <span>Courses</span>
              </Link>
            </div>
          </div>

          <div className="flex items-center gap-2">
            {/* Mobile menu button */}
            <button
              onClick={() => setShowMobileMenu(!showMobileMenu)}
              className="md:hidden p-2 rounded-md text-gray-700 hover:text-primary-600 hover:bg-primary-50"
            >
              {showMobileMenu ? (
                <X className="h-6 w-6" />
              ) : (
                <Menu className="h-6 w-6" />
              )}
            </button>

            {/* User dropdown */}
            <div className="relative">
              <button
                onClick={() => setShowDropdown(!showDropdown)}
                className="flex items-center space-x-3 focus:outline-none"
              >
                <div className="flex items-center space-x-2">
                  <div className="bg-primary-100 p-2 rounded-full">
                    <User className="h-5 w-5 text-primary-600" />
                  </div>
                  <div className="hidden sm:block text-left">
                    <p className="text-sm font-medium text-gray-700">
                      {user?.first_name} {user?.last_name}
                    </p>
                    <p className="text-xs text-gray-500 capitalize">
                      {user?.role}
                    </p>
                  </div>
                </div>
              </button>

              {showDropdown && (
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-1 border border-gray-200">
                  <Link
                    to="/profile"
                    className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    onClick={() => setShowDropdown(false)}
                  >
                    <User className="h-4 w-4 mr-2" />
                    Profile
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="w-full flex items-center px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                  >
                    <LogOut className="h-4 w-4 mr-2" />
                    Logout
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Mobile Navigation Menu */}
        {showMobileMenu && (
          <div className="md:hidden pb-4 pt-2 border-t border-gray-200">
            <div className="space-y-1">
              <Link
                to="/dashboard"
                onClick={closeMobileMenu}
                className="flex items-center space-x-2 px-3 py-3 rounded-md text-base font-medium text-gray-700 hover:text-primary-600 hover:bg-primary-50"
              >
                <LayoutDashboard className="h-5 w-5" />
                <span>Dashboard</span>
              </Link>
              <Link
                to="/courses"
                onClick={closeMobileMenu}
                className="flex items-center space-x-2 px-3 py-3 rounded-md text-base font-medium text-gray-700 hover:text-primary-600 hover:bg-primary-50"
              >
                <BookOpen className="h-5 w-5" />
                <span>Courses</span>
              </Link>
              
              {/* Mobile user info */}
              <div className="sm:hidden pt-3 mt-3 border-t border-gray-200">
                <div className="px-3 py-2 text-sm text-gray-500">
                  Signed in as
                </div>
                <div className="px-3 py-2">
                  <p className="text-sm font-medium text-gray-900">
                    {user?.first_name} {user?.last_name}
                  </p>
                  <p className="text-xs text-gray-500 capitalize">
                    {user?.role}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
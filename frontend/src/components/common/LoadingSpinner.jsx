// src/components/common/LoadingSpinner.jsx
import { Loader2 } from 'lucide-react';

const LoadingSpinner = ({ size = 'md', fullScreen = false }) => {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
  };

  if (fullScreen) {
    return (
      <div className="fixed inset-0 bg-white bg-opacity-75 flex items-center justify-center z-50">
        <div className="text-center">
          <Loader2 className={`${sizeClasses[size]} animate-spin text-primary-600 mx-auto`} />
          <p className="mt-2 text-sm text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-center items-center p-4">
      <Loader2 className={`${sizeClasses[size]} animate-spin text-primary-600`} />
    </div>
  );
};

export default LoadingSpinner;
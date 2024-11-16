import { Outlet } from "react-router-dom";

/**
 * A layout component for unauthenticated users.
 * 
 * This component provides a full-screen layout with a centered container
 * for displaying content. The background is styled with an svg background
 * image and a central content container with padding containing an Outlet component.
 * 
 * @layout
 * @returns {JSX.Element} The layout component for unauthenticated users.
 */
export const UnauthenticatedLayout = (): JSX.Element => {
  return (
    <div className="h-screen flex flex-col items-center justify-center bg-root-background bg-cover">
      <div className="p-8 bg-gray-600 rounded-md shadow-xl">
        <Outlet />
      </div>
    </div>
  );
};

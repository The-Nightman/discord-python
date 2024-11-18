import { Outlet } from "react-router-dom";

export const AuthenticatedLayout = () => {
  return (
    <main className="flex flex-col h-screen">
      <div>
        <p>Discord</p>
      </div>
      <div className="flex flex-1 w-full">
        <div className="w-20 bg-red-400">
          <p>servers list</p>
          {/* Template server icon */}
          <div className="group relative flex w-full items-center justify-center">
            <div className="absolute left-0 bg-white h-3 w-1 rounded-r-full transition-all group-hover:h-5" />
            <div className="bg-gray-500 h-12 w-12 rounded-[50%] transition-all group-hover:rounded-xl" />
          </div>
          {/*  */}
        </div>
        <div className="flex flex-row flex-1 bg-green-400">
          <Outlet />
        </div>
      </div>
    </main>
  );
};

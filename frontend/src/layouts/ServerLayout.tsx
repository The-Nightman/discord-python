export const ServerLayout = () => {
  return (
    <div className="flex flex-col w-[15rem]">
      <div className="flex-1 bg-blue-400">
        <p>Server channels</p>
      </div>
      <div className="flex flex-row h-14 px-2 items-center justify-between bg-purple-400 ">
        <div className="flex items-center gap-2">
          <div className="bg-red-500 w-10 h-10 rounded-full" />
          <p>Username</p>
        </div>
        <div className="bg-red-500 w-10 h-10">
            {/* other controls */}
            <p>icon</p>
        </div>
      </div>
    </div>
  );
};

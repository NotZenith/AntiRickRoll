export const GridBackground = () => {
  return (
    <div className="absolute inset-0 z-[-1] overflow-hidden">
      <div
        className="absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage: `linear-gradient(#fff 1px, transparent 1px), linear-gradient(90deg, #fff 1px, transparent 1px)`,
          backgroundSize: \'40px 40px\',
        }}
      />
      <div
        className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent"
      />
    </div>
  );
};

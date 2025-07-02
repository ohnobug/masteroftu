const TDSBg = () => {
  return (
    <div className="absolute inset-0 z-[-1]">
      <div className="absolute inset-0 bg-gradient-to-b from-cyan-200 via-teal-300 to-cyan-200 opacity-40"></div>
      <img
        src="https://bing.img.run/rand_uhd.php"
        alt="Starry sky texture"
        className="w-full h-full object-cover opacity-50 mix-blend-overlay"
      />
    </div>
  );
};


export default TDSBg;

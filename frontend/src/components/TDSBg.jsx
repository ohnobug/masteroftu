import { useEffect, useState } from "react";
import { useLocation } from "react-router";

const TDSBg = () => {
  const location = useLocation();

  const [bg, setBg] = useState("https://bing.img.run/rand_uhd.php");

  useEffect(() => {
    setBg("https://bing.img.run/rand_uhd.php" + `?t=${new Date().getTime()}`);
  }, [location]);

  return (
    <div className="absolute inset-0 z-[-1]">
      <div className="absolute inset-0 bg-gradient-to-b from-cyan-200 via-teal-300 to-cyan-200 opacity-40"></div>
      <img
        src={bg}
        alt="Starry sky texture"
        className="w-full h-full object-cover opacity-50 mix-blend-overlay"
      />
    </div>
  );
};

export default TDSBg;

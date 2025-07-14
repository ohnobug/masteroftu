import { useEffect } from "react";
import { useLocation } from "react-router";

const TDSFooter = () => {
  const location = useLocation();

  useEffect(() => {}, [location]);

  return (
    <>
      {location.pathname !== "/learning_paths" ? (
        <footer className="relative bottom-0 left-0 w-full p-4 z-20 mt-20 text-center">
          <div className="relative text-white/70 text-xs md:text-sm z-20">
            <span className="mb-1">© 2025 智能客服. All Rights Reserved.</span>
            <a
              href="https://beian.miit.gov.cn/"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:underline"
            >
              鲁ICP备2023025435号-3
            </a>
          </div>

          <div className="absolute bottom-0 left-0 w-full h-24 md:h-32 z-10">
            <svg
              viewBox="0 0 1440 120"
              preserveAspectRatio="none"
              className="w-full h-full"
            >
              <path
                d="M0,64 C240,128 480,32 720,64 C960,96 1200,0 1440,32 L1440,120 L0,120 Z"
                fill="#0c0c2c"
              ></path>
            </svg>
          </div>
        </footer>
      ) : (
        <footer
          className="relative bottom-0 left-0 w-full p-10 z-20 text-center"
          style={{ background: "rgb(12, 12, 44)" }}
        >
          <div className="relative text-white/70 text-xs md:text-sm z-20">
            <span className="mb-1">© 2025 智能客服. All Rights Reserved.</span>
            <a
              href="https://beian.miit.gov.cn/"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:underline"
            >
              鲁ICP备2023025435号-3
            </a>
          </div>
        </footer>
      )}
    </>
  );
};

export default TDSFooter;

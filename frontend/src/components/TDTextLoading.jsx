import { useEffect, useState, useRef } from "react";

export const TDTextLoading = (props) => {
    const [dot, setDot] = useState(1);
    const timer = useRef(null);

    useEffect(() => {
        timer.current = setTimeout(() => {
            if (dot === 5) {
                setDot(1);
            } else {
                setDot(dot + 1);
            }
        }, 300);

        return () => {
            clearTimeout(timer.current);
        }
    }, [dot]);

    return (
        <div style={{ width: "85px" }}>
            {props.text}{".".repeat(dot)}
        </div>
    );
}


import React from "react";

type CardProps = {
    width?: string;
    height?: string;
    additionalClasses?: string;
    children: React.ReactNode;
};

const Card = ({ width, height, additionalClasses, children }: CardProps) => {
    return (
        <div className={`w-${width || "100"} h-${height || "auto"} ${additionalClasses} d-flex flex-column text-light p-4 rounded-4 `}>
            {children}
        </div>
    );
};

export default Card;
import React from "react";

type DropdownFieldProps = {
    value: string;
    setValue: (value: string) => void;
    label?: string;
    required?: boolean;
    disabled?: boolean;
    children: React.ReactNode;
};

const DropdownField = ({ value, setValue, label, required, disabled, children }: DropdownFieldProps) => {
    return (
        <div className="w-100 text-light mb-2">
            {label && <label className="w-100 text-start ps-2 pb-2">{label}</label>}
            <select
                className="w-100 bg-darker text-light rounded-pill px-3 py-2 border-0"
                value={value}
                onChange={(e) => setValue(e.target.value)}
                required={required}
                disabled={disabled}
            >
                {children}
            </select>
        </div>
    );
};

export default DropdownField;

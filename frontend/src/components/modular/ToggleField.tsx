type ToggleFieldProps = {
    value: boolean;
    setValue: (value: boolean) => void;
    type?: string;
    label?: string;
    required?: boolean;
    disabled?: boolean;
};

const ToggleField = ({ value, setValue, type, label, required, disabled }: ToggleFieldProps) => {

    return (
            <div className="form-check w-100 text-start">
                <input
                    className="form-check-input"
                    type={type || "checkbox"}
                    checked={value}
                    onChange={() => setValue(!value)}
                    required={required}
                    disabled={disabled}
                />
                <label className="form-check-label">
                    {label}
                </label>
            </div>
    );
};

export default ToggleField;

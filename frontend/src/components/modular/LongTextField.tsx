type LongTextFieldProps = {
    value: string;
    setValue: (value: string) => void;
    placeholder?: string;
    autoComplete?: string;
    label?: string;
    required?: boolean;
    disabled?: boolean;
    rows?: number;
};

const LongTextField = ({ value, setValue, placeholder, autoComplete, label, required, disabled, rows = 3 }: LongTextFieldProps) => {

    return (
        <div className="w-100 text-light mb-2">
            {label && <label className="w-100 text-start ps-2 pb-2">{label}</label>}
            <textarea
                className="w-100 bg-darker text-light rounded-4 p-3 border-0 resize-vertical"
                placeholder={placeholder}
                value={value}
                autoComplete={autoComplete}
                onChange={(e) => setValue(e.target.value)}
                required={required}
                disabled={disabled}
                rows={rows}
            />
        </div>
    );
};

export default LongTextField;

type TextFieldProps = {
    value: string;
    setValue: (value: string) => void;
    placeholder?: string;
    autoComplete?: string;
    type?: string;
    label?: string;
    required?: boolean;
    disabled?: boolean;
};

const TextField = ({ value, setValue, placeholder, autoComplete, type, label, required, disabled }: TextFieldProps) => {

    return (
        <div className="w-100 text-light mb-2">
            <label className="w-100 text-start ps-2 pb-2">{label}</label>
            <input
                className="w-100 bg-darker text-light rounded-pill px-3 py-2 border-0"
                type={type}
                placeholder={placeholder}
                value={value}
                autoComplete={autoComplete}
                onChange={(e) => setValue(e.target.value)}
                required={required}
                disabled={disabled}
            />
        </div>
    );
};

export default TextField;

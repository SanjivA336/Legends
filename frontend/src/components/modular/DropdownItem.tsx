type DropdownItemProps = {
    value: string;
    label: string;
};

const DropdownItem = ({ value, label }: DropdownItemProps) => {
    return (
        <option value={value}>
            {label}
        </option>
    );
};

export default DropdownItem;

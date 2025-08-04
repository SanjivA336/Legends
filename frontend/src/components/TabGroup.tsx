import ButtonField from "@components/fields/ButtonField";

type TabGroupProps = {
    tabNumber: number;
    setTabNumber: (tabNumber: number) => void;

    disabled?: boolean;

    orientation?: "horizontal" | "vertical";
    rounding?: "0" | "1" | "2" | "3" | "4" | "5" | "pill";

    tabNames: Array<string>;
};

const TabGroup = ({ tabNumber, setTabNumber, disabled = false, orientation="horizontal", rounding="3", tabNames }: TabGroupProps) => {

    const changeTab = (index: number) => {
        if (!disabled) {
            setTabNumber(index);
        }
    }

    return (
        <div className="w-100 text-light d-flex flex-column my-2">
            <div
                className={[
                    "w-100 d-flex flex-row gap-2 my-2 p-2",
                    orientation === "vertical" ? "flex-column" : "w-100 flex-row",
                    rounding === "pill" ? "rounded-pill" : "rounded-" + rounding,
                ].join(" ")}
            >
                {tabNames.map((tabName, index) => (
                    <ButtonField
                        key={index}
                        onClick={() => changeTab(index)}
                        disabled={disabled}
                        color={tabNumber === index ? (disabled ? "light" : "primary") : "dark"}
                        rounding={rounding}
                        caps="both"
                        className={`justify-content-center p-3 ${disabled ? "text-dark" : "text-light"}`}
                    >
                        <h4 className="m-0">{tabName}</h4>
                    </ButtonField>
                ))}
            </div>
        </div>
    );
};

export default TabGroup;

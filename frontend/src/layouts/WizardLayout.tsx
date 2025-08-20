import TabGroup from "@components/TabGroup";
import ButtonField from "@/components/fields/ButtonField";
import MessageBox from "@/components/MessageBox";

type DetailLayoutProps = {
    currentTab: number;
    setCurrentTab: (tab: number) => void;

    tabs: string[];
    title: string;

    children: React.ReactNode;

    onSave: () => void;
    onReset: () => void;
    onExit: () => void;
    isDirty: boolean;
    isLoading?: boolean;
};

export default function DetailLayout({ currentTab, setCurrentTab, tabs, title, children, onSave, onReset, onExit, isDirty, isLoading }: DetailLayoutProps) {

    return (
        <div className="w-100 vh-100 d-flex flex-column align-items-center justify-content-between p-2 mt-4">
            <div className="w-100 d-flex flex-row align-items-center justify-content-between">
                <div className="col-3 col-md-2 p-2">
                    {onExit && (
                        <ButtonField
                            onClick={onExit}
                            type="button"
                            color="dark"
                            rounding="3"
                            className="w-100"
                            loading={isLoading}
                            disabled={isDirty || false}
                        >
                            <h5 className="w-100 p-3 text-light text-center m-0">Exit to Library</h5>
                        </ButtonField>
                    )}
                </div>
                <div className="col-9 col-md-10 p-2">
                    <h3 className="w-100 p-3 text-light text-center m-0 bg-darker border-darkish rounded-4">{title}</h3>
                </div>
            </div>

            <div className="w-100 d-flex flex-row flex-grow-1 align-items-start justify-content-between overflow-hidden">
                {/* Tabs column */}
                <div className="mh-100 col-3 col-md-2 p-2 d-flex flex-column overflow-y-auto scrollbar-hidden">
                    <TabGroup
                        tabNumber={currentTab}
                        setTabNumber={setCurrentTab}
                        tabNames={tabs}
                        orientation="vertical"
                        rounding="3"
                        disabled={false}
                    />
                </div>

                {/* Content column */}
                <div className="mh-100 col-9 col-md-10 p-2 d-flex flex-column overflow-y-auto scrollbar-hidden">
                    {children}
                </div>
            </div>

            <div className="w-100 d-flex flex-row align-items-center justify-content-between p-2">
                <ButtonField
                    onClick={onReset}
                    color="danger"
                    rounding="3"
                    className="col-4 col-md-3 p-3"
                    loading={isLoading}
                    disabled={!isDirty}
                >
                    Reset
                </ButtonField>
                {isDirty && (
                    <div className="col-3 col-md-5 text-warning text-center">
                        <MessageBox warning="You have unsaved changes."/>
                    </div>
                )}
                <ButtonField
                    onClick={onSave}
                    color="primary"
                    rounding="3"
                    className="col-4 col-md-3 p-3"
                    loading={isLoading}
                    disabled={!isDirty}
                >
                    Save
                </ButtonField>
            </div>
        </div>
    );
}

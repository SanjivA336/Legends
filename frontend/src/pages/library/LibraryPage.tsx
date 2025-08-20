import { useNavigate, useSearchParams } from "react-router-dom";
import { useEffect, useState } from "react";

import BaseLayout from "@/layouts/BaseLayout";
import WorldLibrary from "@features/library/WorldLibrary";
import BlueprintsLibrary from "@features/library/BlueprintLibrary";
import TabGroup from "@components/TabGroup";

export default function LibraryPage() {
    const navigate = useNavigate();

    const [searchParams] = useSearchParams();
    const tabParam = searchParams.get("tab");
    const initialTab = parseInt(tabParam || "0", 10);

    const [currentTab, setCurrentTab] = useState(initialTab);

    useEffect(() => {
        // Keep in sync if URL changes manually
        if (!isNaN(initialTab) && initialTab !== currentTab) {
            setCurrentTab(initialTab);
        }
    }, [tabParam]);

    useEffect(() => {
        // Update the URL when currentTab changes
        navigate(`/library?tab=${currentTab}`, { replace: true });
    }, [currentTab]);

    const tabs = ["Worlds", "Campaigns", "Blueprints"];

    return (
        <BaseLayout>
            <div className="d-flex flex-column gap-3 w-100 h-100">

                <h1 className="text-center text-light m-0 p-4">Your Library</h1>

                <TabGroup
                    tabNumber={currentTab}
                    setTabNumber={setCurrentTab}
                    tabNames={tabs}
                    orientation="horizontal"
                    rounding="3"
                    disabled={false}
                />

                <hr className="text-light px-3 py-0 my-1" />

                <div className="w-100 h-auto d-flex flex-column mt-3 align-items-center">
                    {currentTab === 0 && <WorldLibrary />}
                    {currentTab === 1 && <div>Campaigns Content</div>}
                    {currentTab === 2 && <BlueprintsLibrary />}
                </div>
            </div>
        </BaseLayout>
    );
}

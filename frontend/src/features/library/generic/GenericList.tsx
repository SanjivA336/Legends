import { useEffect, useState } from "react";

import ButtonField from "@/components/fields/ButtonField";
import ShortTextField from "@/components/fields/ShortTextField";
import DropdownField from "@/components/fields/DropdownField";
import NumberField from "@/components/fields/NumberField";

import Loading from "@/components/Loading";

import DeletePopup from "@/components/DeletePopup";

type GenericListProps<T> = {
    itemName?: string;
    items: T[];
    refresh?: () => void;
    openEditor?: (item: T) => void;
    openCreator?: () => void;
    renderDetails: (item: T) => React.ReactNode;

    loading?: boolean;

    search?: boolean;
    getItemName?: (item: T) => string;
    viewSelector?: boolean;
    defaultView?: "grid" | "list";
    limitSelector?: boolean;
    defaultLimit?: number;
    pagination?: boolean;

    highlighted?: T | null;
    setHighlighted?: (item: T | null) => void;

    children?: React.ReactNode;
}

export function GenericList<T>({ itemName="item", items, refresh, openEditor, openCreator, renderDetails, loading, search = false, getItemName, viewSelector = false, defaultView = "grid", limitSelector = false, defaultLimit = 8, pagination = false, highlighted = null, setHighlighted, children }: GenericListProps<T>) {
    const [searchQuery, setSearchQuery] = useState<string>("");
    const [filteredItems, setFilteredItems] = useState<T[]>(items);
    const [view, setView] = useState<"grid" | "list">(defaultView);
    const [limit, setLimit] = useState<number>(defaultLimit);

    const [page, setPage] = useState<number>(0);
    const [maxPages, setMaxPages] = useState<number>(Math.ceil(items.length / (limit || items.length)));
    
    const [showDelete, setShowDelete] = useState<boolean>(false);


    const limitOptions = [4, 8, 12, 16, 20, 24, 32, 50, 100];

    const filterItems = () => {
        if (!searchQuery) {
            setFilteredItems(items);
        }
        else {
            const query = searchQuery.toLowerCase();
            const filtered = items.filter(item =>
                getItemName ? getItemName(item).trim().toLowerCase().includes(query.trim().toLowerCase()) : false
            );
            setFilteredItems(filtered);
        }
    }

    useEffect(() => {
        filterItems();
    }, [searchQuery, items]);

    useEffect(() => {
        setMaxPages(Math.ceil(filteredItems.length / limit));
    }, [filteredItems, limit]);



    return (
        <div className="w-100 h-100 align-items-center d-flex flex-column gap-2">
            {search && (
                <div className="w-100 d-flex flex-row mb-2">
                    {refresh && (
                        <div className="w-25 px-1">
                            <ButtonField
                                onClick={refresh}
                                loading={loading}
                                color="dark"
                                rounding="pill"
                                className="p-2"
                            >
                                Refresh
                            </ButtonField>
                        </div>
                    )}

                    <div className="w-100 px-1">
                        <ShortTextField
                            value={searchQuery}
                            setValue={setSearchQuery}
                            placeholder={`Search ${itemName}s by name...`}
                            prepend="🔍︎"
                            clearable
                        />
                    </div>

                    {(viewSelector || limitSelector) && (
                        <div className="w-50 d-flex flex-row px-1 gap-2 py-0 m-0">
                            {viewSelector && (
                                <DropdownField
                                    value={view}
                                    setValue={setView}
                                    prepend="View"
                                    options={["grid", "list"]}
                                    optionValue={(option) => option}
                                    optionLabel={(option) => option.charAt(0).toUpperCase() + option.slice(1)}
                                />
                            )}
                            {limitSelector && (
                                <DropdownField
                                    value={limit}
                                    setValue={setLimit}
                                    prepend="Limit"
                                    options={limitOptions}
                                    optionValue={(option) => option}
                                    optionLabel={(option) => option.toString()}
                                />
                            )}
                        </div>
                    )}

                    {openCreator && (
                        <div className="w-25 px-1">
                            <ButtonField
                                onClick={openCreator}
                                loading={loading}
                                color="primary"
                                rounding="pill"
                                className="p-2"
                            >
                                Create
                            </ButtonField>
                        </div>
                    )}

                    {children && (
                        <div className="w-25 px-1">
                            {children}
                        </div>
                    )}
                </div>
            )}

            {loading ? (
                <Loading message={`Loading ${itemName}s...`} />
            ) : items.length === 0 ? (
                <div className="text-light text-center">
                    <p>No {itemName}s found.</p>
                    {openCreator && (
                        <ButtonField onClick={openCreator}>
                            Create one now!
                        </ButtonField>
                    )}
                </div>
            ) : items.length > 0 && filteredItems.length === 0 ? (
                <div className="text-light text-center">
                    <p>No {itemName}s found matching your search.</p>
                    {openCreator && (
                        <ButtonField onClick={openCreator}>
                            Create one now!
                        </ButtonField>
                    )}
                </div>
            ) : (
                <div className="w-100 h-100 d-flex flex-column align-items-center">
                    <div className={`w-100 d-flex flex-${view === "grid" ? "row flex-wrap" : "column"}`}>
                        {filteredItems.slice(page * limit, (page + 1) * limit).map((item, index) => (
                            <div key={index} className={`${view === "grid" ? "col-lg-3 col-md-4 col-sm-6" : "col-12"} gap-2 p-2`}>
                                <div 
                                    className={["w-100 h-100 justify-content-between gap-2 p-3 rounded-3 d-flex overflow-hidden",
                                        `flex-${view === "grid" ? "column" : "row"}`,
                                        item === highlighted ? "bg-primary shadow-lg" : "bg-dark shadow"
                                    ].join(" ")} 
                                    onClick={() => setHighlighted?.(item)}
                                >
                                    {renderDetails(item)}
                                    <span className="w-100 d-flex flex-row gap-2">
                                        {openEditor && (
                                            <ButtonField onClick={() => openEditor(item)}
                                                loading={loading}
                                                color={item === highlighted ? "light" : "primary"}
                                                rounding="2"
                                                className={`px-4 w-${view === "grid" ? 100 : 25}`} >
                                                Edit
                                            </ButtonField>
                                        )}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                    {pagination && (
                        <div className="w-50 d-flex flex-row justify-content-center align-items-center gap-2 mt-3">
                            <span className="w-100 text-light text-center d-flex flex-row align-items-center justify-content-center">
                                Page 
                                <div className="w-50 mx-2">
                                    <NumberField
                                        value={page + 1}
                                        setValue={(value) => setPage(value - 1)}
                                        min={1}
                                        max={maxPages}
                                        incrementer
                                    />
                                </div>
                                of {maxPages}
                            </span>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default GenericList;

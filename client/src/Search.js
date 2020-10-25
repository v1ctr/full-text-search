import React, { useState } from 'react';
import { Input, AutoComplete, Select, Typography } from 'antd';
import axios from "axios";
import { debounce } from 'lodash';

const Option = Select.Option;
const { Text } = Typography;

const searchResult = (query) => {
    return new Array()
        .join('.')
        .split('.')
        .map((item, idx) => {
            const category = `${query}${idx}`;
            return {
                value: category,
                label: (
                    <div
                        style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                        }}
                    >
                        <span>
                            Found {query} on{' '}
                        </span>
                    </div>
                ),
            };
        });
};

function Search() {
    const [options, setOptions] = useState([]);

    const handleSearchDebounced = debounce(handleSearch, 100);

    const renderLabel = (item, query) => {

        if (query) {

            let title_index = item.title.toLowerCase().indexOf(query.toLowerCase());
            let description_index = item.description.toLowerCase().indexOf(query.toLowerCase());

            if (title_index !== -1 && description_index !== -1) {

                let length = query.length;

                let title_prefix = item.title.substring(0, title_index);
                let title_suffix = item.title.substring(title_index + length);
                let title_match = item.title.substring(title_index, title_index + length);

                let description_prefix = item.description.substring(0, description_index);
                let description_suffix = item.description.substring(description_index + length);
                let description_match = item.description.substring(description_index, description_index + length);

                return (
                    <div>
                        <h3>{title_prefix}<Text mark>{title_match}</Text>{title_suffix}</h3>
                        <span>{description_prefix}<Text mark>{description_match}</Text>{description_suffix}</span>
                    </div>
                );
            }
        }

        return (
            <div>
                <h3>{item.title}</h3>
                <span>{item.description}</span>
            </div>
        );
    }

    async function handleSearch(value) {
        if (!value) return;
        try {
            let result = await axios.get('/api/search', {
                params: {
                    search: value
                }
            });
            if (result.status === 200) {
                setOptions(result.data.map((show) => {
                    return {
                        value: show.title,
                        label: renderLabel(show, value)
                    };
                }))
            } else {
                console.log("failed");
            }
        } catch (error) {
            console.log(error);
        }
        // setOptions(value ? searchResult(value) : []);
    };

    const onSelect = (value) => {
        console.log('onSelect', value);
    };

    return (
        <AutoComplete
            dropdownMatchSelectWidth={252}
            style={{
                width: '100%',
            }}
            options={options}
            onSelect={onSelect}
            onSearch={handleSearchDebounced}
        >
            <Input.Search size="large" placeholder="input here" enterButton />
        </AutoComplete>
    );
};

export default Search;
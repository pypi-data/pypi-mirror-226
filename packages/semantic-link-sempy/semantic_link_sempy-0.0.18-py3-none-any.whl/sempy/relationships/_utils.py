import pandas as pd
import inspect
import warnings

from typing import Dict, List, Optional, Set, Tuple, Union


def _to_dataframe_dict(
    tables: Union[Dict[str, pd.DataFrame], List[pd.DataFrame]],
) -> Dict[str, pd.DataFrame]:

    if isinstance(tables, (tuple, list)):
        result = {}
        for i in range(len(tables)):
            # Try to find the name of the element in the session or use the index as name
            # if a match cannot be found
            var_name = _find_variable_name_up_the_stack(tables[i])
            if var_name:
                result[var_name] = tables[i]
            else:
                result[f"[{i}]"] = tables[i]
    elif isinstance(tables, dict):
        result = tables
    else:
        raise ValueError(f"Argument \"tables\" must be a dictionary of dataframes by name or a list of dataframes: {type(tables)}")

    if not all(isinstance(e, pd.DataFrame) for e in result.values()):
        raise ValueError("All \"tables\" elements must be pandas dataframes or derived")

    return result


def _find_variable_name_up_the_stack(obj):
    frame = inspect.currentframe().f_back
    while frame is not None:
        for name, value in frame.f_locals.items():
            if value is obj:
                return name
        frame = frame.f_back
    return None


def _to_exclude_tuples(
    exclude: Union[List[Tuple[str]], pd.DataFrame]
) -> Optional[Set[Tuple[str]]]:
    msg = "must be a list of tuples(from_table, from_column, to_table, to_column)"
    if exclude is None:
        result = None
    elif isinstance(exclude, list):
        for t in exclude:
            if not isinstance(t, tuple):
                raise ValueError(f"Invalid type {type(t)} of an element fo \"exclude\", which {msg}")
            if len(t) != 4:
                raise ValueError(f"Invalid len {len(t)} of an element fo \"exclude\", which {msg}")
        result = set(exclude)
    elif isinstance(exclude, pd.DataFrame):
        result = exclude[["from_table", "from_column", "to_table", "to_column"]]
        result = set(result.itertuples(index=False, name=None))   # type: ignore
    else:
        raise ValueError(f"Argument \"exclude\" {msg}, and not {type(exclude)}")
    return result


def _is_key_missing(rel, table_columns, action):

    def _execute_action(msg: str):
        if action == 'raise':
            raise ValueError(f"{msg}. To suppress this exception use \"missing_key_errors\" of ['warn', 'ignore']")
        elif action == 'warn':
            warnings.warn(msg)
        return True

    if rel.from_table not in table_columns:
        return _execute_action(f"Table '{rel.from_table}' not in \"tables\"")
    if rel.to_table not in table_columns:
        return _execute_action(f"Table '{rel.to_table}' not in \"tables\"")
    if rel.from_column not in table_columns[rel.from_table]:
        return _execute_action(f"Column '{rel.from_column}' not in table '{rel.from_table}'")
    if rel.to_column not in table_columns[rel.to_table]:
        return _execute_action(f"Column '{rel.to_column}' not in table '{rel.to_table}'")
    return False

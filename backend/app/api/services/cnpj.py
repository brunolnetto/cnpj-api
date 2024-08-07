from fastapi import HTTPException, Depends
from typing import Union

from backend.app.repositories.cnpj import CNPJRepository
from backend.app.utils.misc import is_number, are_numbers
from backend.app.api.utils.cnpj import are_cnpj_str_valid
from backend.app.setup.config import settings
from backend.app.api.dependencies.cnpj import CNPJRepositoryDependency
from backend.app.api.models.cnpj import CNPJ
from backend.app.api.utils.cnpj import parse_cnpj_str, format_cnpj
from backend.app.api.utils.misc import check_limit_and_offset
from backend.app.api.models.cnpj import CNPJBatch
from backend.app.api.models.base import BatchModel
from backend.app.setup.logging import logger
from .constants import STATES_BRAZIL

# Types
CodeType = Union[str, int]


def cnpj_str_to_obj(cnpj_str: str):
    """
    Converts a CNPJ string to a CNPJ object.

    Args:
        cnpj_str (str): The CNPJ string to convert.

    Returns:
        CNPJ: The CNPJ object.
    """

    cnpj_list = parse_cnpj_str(cnpj_str)
    return CNPJ(*cnpj_list)


class CNPJService:
    def __init__(self, cnpj_repository: CNPJRepository):
        self.repository: CNPJRepository = cnpj_repository

    async def get_cnaes(
        self, limit: int = 10, offset: int = 0, enable_pagination: bool = True
    ):
        """
        Get a list of CNAEs from the database.

        Parameters:
        - limit: The maximum number of CNAEs to return.
        - offset: The number of cnaes to skip.
        - enable_pagination: Flag to allow pagination

        Returns:
        - A list of CNAEs as dictionaries.
        """
        try:
            limit, offset = check_limit_and_offset(limit, offset)

            cnaes = self.repository.get_cnaes(
                limit=limit, offset=offset, enable_pagination=enable_pagination
            )

            return cnaes

        except Exception as e:
            logger.error(f"Error getting CNAEs: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

    async def get_cnae_objects(self, cnae_code_batch: BatchModel):
        """
        Get CNAE objects from a list of codes.

        Parameters:
        - cnae_code_batch: The CNAE code batch to search for.

        Returns:
        - A list with the CNAE objects.
        """
        try:
            cnae_code_list = set(list(cnae_code_batch.batch))

            if not are_numbers(cnae_code_list):

                def not_number_map(candidate):
                    return not is_number(candidate)

                not_numbers = list(filter(not_number_map, cnae_code_list))
                raise ValueError(f"CNAE codes {not_numbers} are not numbers.")

            cnaes = self.repository.get_cnae_list(cnae_code_list)
        except Exception as e:
            logger.error(f"Error getting CNAEs: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

        if len(cnaes) == 0:
            return {"message": f"CNAE codes {cnae_code_list} not found."}

        return cnaes

    async def get_cnae_description(self, cnae_code: CodeType):
        """
        Get the description of a CNAE code.

        Parameters:
        - cnae_code: The CNAE code to search for.

        Returns:
        - A dictionary with the CNAE description.
        """
        try:
            if not is_number(cnae_code):
                raise ValueError(f"CNAE code {cnae_code} is not a number.")

            cnae_code_list = [cnae_code]
            cnaes = self.repository.get_cnae_list(cnae_code_list)
        except Exception as e:
            logger.error(f"Error getting CNAEs: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

        if len(cnaes) == 0:
            return {"message": f"CNAE code {cnae_code} not found."}

        return cnaes[0]

    async def get_cnpjs_with_cnae(
        self, cnae_code: CodeType, limit: int = 10, offset: int = 0
    ):
        """
        Get a list of establishments with a given CNAE code.

        Parameters:
        - cnae_code: The CNAE code to search for.
        - limit: The maximum number of establishments to return.
        - offset: The number of establishments to skip.

        Returns:
        - A list of establishments as dictionaries.
        """
        try:
            limit, offset = check_limit_and_offset(limit, offset)

            if not is_number(cnae_code):
                raise ValueError(f"CNAE code {cnae_code} is not a number.")

            cnaes = self.repository.get_cnae(cnae_code)

            if not cnaes:
                raise ValueError(f"There isn't CNAE code {cnae_code}.")

            cnae_code_list = [cnae_code]
            cnpjs = self.repository.get_cnpjs_by_cnaes(
                cnae_code_list, limit=limit, offset=offset
            )

        except Exception as e:
            logger.error(f"Error getting CNPJs with CNAE: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

        if len(cnpjs) == 0:
            return {
                "message": f"There are no establishents with CNAE code {cnae_code}."
            }

        return cnpjs

    async def get_cnpjs_by_cnaes(
        self, cnae_batch: BatchModel, limit: int = 10, offset: int = 0
    ):
        """
        Get a list of establishments with the specified CNAE codes.

        Parameters:
        - cnae_batch: The batch of CNAE codes to search for.
        - limit: The maximum number of establishments to return.
        - offset: The number of establishments to skip.

        Returns:
        - A list of establishments as dictionaries.
        """
        try:
            cnae_list = list(set(cnae_batch.batch))

            if not are_numbers(cnae_list):

                def not_number_map(candidate):
                    return not is_number(candidate)

                not_numbers = list(filter(not_number_map, cnae_list))
                raise ValueError(f"CNAE codes {not_numbers} are not numbers.")

            establishments = self.repository.get_cnpjs_by_cnaes(
                cnae_list, limit=limit, offset=offset
            )

        except Exception as e:
            logger.error(f"Error getting CNPJs by CNAEs: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

        if len(establishments) == 0:
            return {
                "message": f"There are no establishments with CNAE codes {cnae_list}."
            }

        return establishments

    async def get_city_candidates(self, city_names: BatchModel):
        """
        Get a list of city candidates.

        Parameters:
        - city_name: The city name to search for.
        - limit: The maximum number of cities to return.

        Returns:
        - A list of cities as dictionaries.
        """
        try:
            city_names_list = list(set(city_names.batch))
            city_candidates = self.repository.get_city_candidates(city_names_list)

            return city_candidates

        except Exception as e:
            logger.error(f"Error getting city candidates: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

    async def get_cnpjs_by_states(
        self, state_batch: BatchModel, limit: int = 10, offset: int = 0
    ):
        """
        Get a list of establishments in the specified states.

        Parameters:
        - state_batch: The batch of states to search for.

        Returns:
        - A list of establishments as dictionaries.
        """
        try:
            states = list(set(map(str.upper, state_batch.batch)))
            invalid_states = set(states) - set(STATES_BRAZIL)
            set(states) - invalid_states

            if invalid_states:
                raise ValueError(f"Invalid states: {invalid_states}")

            cnpjs_info = self.repository.get_cnpjs_by_states(
                states, limit=limit, offset=offset
            )

        except Exception as e:
            logger.error(f"Error getting CNPJs in states: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

        if len(cnpjs_info) == 0:
            return {"message": f"There are no cnpjs in states {states}."}

        return cnpjs_info

    async def get_city(self, city_code: CodeType):
        """
        Get the name of a city code.

        Parameters:
        - city_code: The city code to search for.

        Returns:
        - A dictionary with the city name.
        """

        try:
            if not is_number(city_code):
                raise ValueError(f"City code {city_code} is not a number.")

            city = self.repository.get_city(city_code)

        except Exception as e:
            logger.error(f"Error getting city: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

        if len(city) == 0:
            return {"message": f"City code {city_code} not found."}

        return city

    async def get_cities(self, limit: int = 10, offset: int = 0):
        """
        Get a list of cities from the database.

        Parameters:
        - limit: The maximum number of cities to return.

        Returns:
        - A list of cities as dictionaries.
        """
        try:
            limit, offset = check_limit_and_offset(limit, offset)

            return self.repository.get_cities(limit=limit, offset=offset)
        except Exception as e:
            logger.error(f"Error getting cities: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

    async def get_cities_list(self, cities_code_batch: BatchModel):

        try:
            cities_code_list = list(set(cities_code_batch.batch))

            if not are_numbers(cities_code_list):

                def not_number_map(candidate):
                    return not is_number(candidate)

                not_numbers = list(filter(not_number_map, cities_code_list))
                raise ValueError(f"Cities codes {not_numbers} are not numbers.")

            cities_objs = self.repository.get_cities_list(cities_code_list)
        except Exception as e:
            logger.error(f"Error getting cities list: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

        if len(cities_objs) == 0:
            return {"message": f"Cities codes {cities_code_list} not found."}

        return cities_objs

    async def get_company_size_dict(self):
        """
        Get company size dictionary.

        Returns:
        - A dictionary with the company size codes.
        """
        return self.repository.get_company_size_dict()

    async def get_establishment_type_dict(self):
        """
        Get establishment type dictionary.

        Returns:
        - A dictionary with the establishment type codes.
        """
        return self.repository.get_establishment_type_dict()

    async def get_company_situation_dict(self):
        """
        Get company situation dictionary.

        Returns:
        - A dictionary with the company situation codes.
        """
        return self.repository.get_company_situation_dict()

    async def get_legal_nature(self, legal_nature_code: CodeType):
        """
        Get a list of legal natures from the database.

        Parameters:
        - legal_nature_code: Code of the legal nature to search for.

        Returns:
        - A list of legal natures as dictionaries.
        """
        try:
            if not is_number(legal_nature_code):
                raise ValueError(
                    f"Legal nature code {legal_nature_code} is not a number."
                )

            legal_nature_code_list = [legal_nature_code]
            legal_nature_obj_list = self.repository.get_legal_natures_list(
                legal_nature_code_list
            )

        except Exception as e:
            logger.error(f"Error getting legal nature: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

        if len(legal_nature_obj_list) != 1:
            return {"message": f"Legal nature code {legal_nature_code} not found."}

        return legal_nature_obj_list[0]

    async def get_legal_natures(
        self, limit: int = 10, offset: int = 0, enable_pagination: bool = True
    ):
        """
        Get a list of legal natures from the database.

        Parameters:
        - limit: The maximum number of legal natures to return.
        - offset: The number of legal natures to skip.
        - enable_pagination: Flag to allow pagination

        Returns:
        - A list of legal natures as dictionaries.
        """
        try:
            limit, offset = check_limit_and_offset(limit, offset)

            return self.repository.get_legal_natures(
                limit=limit, offset=offset, enable_pagination=enable_pagination
            )
        except Exception as e:
            logger.error(f"Error getting legal natures: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

    async def get_legal_natures_list(self, legal_natures_code_batch: BatchModel):
        """
        Get a list of legal natures from the database.

        Parameters:
        - legal_natures_code_batch: The list of legal nature codes to search for.

        Returns:
        - A list of legal natures as dictionaries.
        """
        try:
            legal_natures_code_list = list(set(legal_natures_code_batch.batch))

            if not are_numbers(legal_natures_code_list):

                def not_number_map(candidate):
                    return not is_number(candidate)

                not_numbers = list(filter(not_number_map, legal_natures_code_list))
                raise ValueError(f"Cities codes {not_numbers} are not numbers.")

            legal_natures_objs = self.repository.get_legal_natures_list(
                legal_natures_code_list
            )
        except Exception as e:
            logger.error(f"Error getting legal natures list: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

        if len(legal_natures_objs) == 0:
            return {
                "message": f"Legal nature codes {legal_natures_code_list} not found."
            }

        return legal_natures_objs

    async def get_registration_status(self, registration_status_code: CodeType):
        """
        Get a registration status from the database.

        Parameters:
        - registration_status_code: The registration status code to search for.

        Returns:
        - A dictionary with the registration status.
        """
        try:
            if not is_number(registration_status_code):
                raise ValueError(
                    f"Registration status code {registration_status_code} is not a number."
                )

            registration_status_code = registration_status_code.strip()
            registration_status_list = [registration_status_code]

            registration_map = self.repository.get_registration_status_list
            registration_status = registration_map(registration_status_list)

        except Exception as e:
            logger.error(f"Error getting registration status: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

        if len(registration_status) == 0:
            return {
                "message": f"Registration status code {registration_status_code} not found."
            }

        return registration_status[0]

    async def get_registration_statuses_list(self, registration_code_batch: BatchModel):
        """
        Get a list of registration statuses from the database.

        Parameters:
        - registration_code_batch: The list of registration status codes to search for.

        Returns:
        - A list of registration statuses as dictionaries.
        """
        try:
            registration_code_list = list(set(registration_code_batch.batch))

            if not are_numbers(registration_code_list):

                def not_number_map(candidate):
                    return not is_number(candidate)

                not_numbers = list(filter(not_number_map, registration_code_list))
                raise ValueError(
                    f"Registration status codes {not_numbers} are not numbers."
                )

            registration_map = self.repository.get_registration_status_list
            registration_status = registration_map(registration_code_list)

        except Exception as e:
            logger.error(f"Error getting registration statuses list: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

        if len(registration_status) == 0:
            return {
                "message": f"Registration status codes {registration_code_list} not found."
            }

        return registration_status

    async def get_registration_statuses(
        self, limit: int = 10, offset: int = 0, enable_pagination: bool = True
    ):
        """
        Get a list of registration statuses from the database.

        Parameters:
        - limit: The maximum number of registration statuses to return.
        - offset: The number of registration statuses to skip.
        - enable_pagination: Enable pagination.

        Returns:
        - A list of registration statuses as dictionaries.
        """
        try:
            limit, offset = check_limit_and_offset(limit, offset)

            return self.repository.get_registration_statuses(
                limit=limit, offset=offset, enable_pagination=enable_pagination
            )
        except Exception as e:
            logger.error(f"Error getting registration statuses: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

    async def get_cnpj_activities(self, cnpj: str):
        """
        Get the activities of a CNPJ number.

        Parameters:
        - cnpj: The CNPJ number to search for.

        Returns:
        - A list of activities associated with the CNPJ.
        """
        try:
            if not is_number(cnpj):
                raise ValueError(
                    f"CNPJ {cnpj} is not a number. Provide only the 14 digits."
                )

            cnpj_obj = cnpj_str_to_obj(cnpj)
            activities = self.repository.get_cnpj_activities(cnpj_obj)

        except Exception as e:
            logger.error(f"Error getting CNPJ activities: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

        if not activities:
            return {"message": f"There are no activities associated with CNPJ {cnpj}."}

        return activities

    async def get_cnpj_partners(self, cnpj: str):
        """
        Get the partners of a CNPJ number.

        Parameters:
        - cnpj: The CNPJ number to search for.

        Returns:
        - A list of partners associated with the CNPJ.
        """
        try:
            if not is_number(cnpj):
                raise ValueError(
                    f"CNPJ {cnpj} is not a number. Provide only the 14 digits."
                )

            cnpj_obj = cnpj_str_to_obj(cnpj)
            cnpj_list = [cnpj_obj]
            cnpj_info = self.repository.get_cnpjs_partners(cnpj_list)

        except Exception as e:
            logger.error(f"Error getting CNPJ partners: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

        if not cnpj_info:
            error = f"There are no partners associated with CNPJ {cnpj}"
            explanation = "It is likely either a sole proprietorship or a legal entity."
            return {"message": f"{error}. {explanation}"}

        return cnpj_info[cnpj_obj.to_raw()]

    async def get_cnpj_company(self, cnpj: str):
        """
        Get the company associated with a CNPJ number.

        Parameters:
        - cnpj: The CNPJ number to search for.

        Returns:
        - A dictionary with information about the company.
        """
        try:
            if not is_number(cnpj):
                raise ValueError(
                    f"CNPJ {cnpj} is not a number. Provide only the 14 digits."
                )

            cnpj_obj = cnpj_str_to_obj(cnpj)
            cnpj_list = [cnpj_obj]

            company_info = self.repository.get_cnpjs_company(cnpj_list)

        except Exception as e:
            logger.error(f"Error getting CNPJ company: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

        if not company_info:
            return {"message": f"There is no company associated with CNPJ {cnpj}."}

        return company_info[cnpj_obj.to_raw()]

    async def get_cnpj_establishment(self, cnpj: str):
        """
        Get the establishment associated with a CNPJ number.

        Parameters:
        - cnpj: The CNPJ number to search for.

        Returns:
        - A dictionary with information about the establishment.
        """

        try:
            if not is_number(cnpj):
                raise ValueError(
                    f"CNPJ {cnpj} is not a number. Provide only the 14 digits."
                )

            cnpj_obj = cnpj_str_to_obj(cnpj)
            cnpjs = [cnpj_obj]

            est_info = self.repository.get_cnpjs_establishment(cnpjs)

        except Exception as e:
            logger.error(f"Error getting CNPJ establishment: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

        if not est_info:
            base_msg = f"There is no establishment associated with CNPJ {cnpj_obj}"
            explanation = f"Try route {settings.API_V1_STR}/cnpj/{cnpj}/company to verify if the CNPJ exists."
            message = f"{base_msg}. {explanation}"

            return {"message": message}

        return est_info[cnpj]

    async def get_cnpj_establishments(self, cnpj: str):
        """
        Get the establishments associated with a CNPJ base (First 8 digits).
        You must provide any full CNPJ number.

        Parameters:
        - cnpj: The CNPJ number to search for.

        Returns:
        - A list of establishments associated with the CNPJ.
        """
        try:
            if not is_number(cnpj):
                raise ValueError(
                    f"CNPJ {cnpj} is not a number. Provide only the 14 digits."
                )

            cnpj_obj = cnpj_str_to_obj(cnpj)
            cnpj_base = cnpj_obj.basico_str

            est_info = self.repository.get_cnpj_establishments(cnpj_obj)

        except Exception as e:
            logger.error(f"Error getting CNPJ establishments: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

        if not est_info:
            return {
                "message": f"There are no establishments associated with CNPJ base {cnpj_base}."
            }

        return est_info

    async def get_cnpjs(
        self,
        state_abbrev: str = "",
        city_name: str = "",
        cnae_code: str = "",
        zipcode: str = "",
        is_all: bool = False,
        limit: int = 10,
        offset: int = 0,
    ): 
        """
        Get a list of CNPJs from the database.

        Parameters:
        - cnpj_batch: The batch of CNPJs to search for.

        Returns:
        - A list of CNPJs as dictionaries.
        """
        remove_quotes=lambda text: text.replace("'", "").replace('"', "")
        
        city_name = remove_quotes(city_name)
        cnae_code = remove_quotes(cnae_code)
        state_abbrev = remove_quotes(state_abbrev)
        zipcode = remove_quotes(zipcode)

        try:
            limit, offset = check_limit_and_offset(limit, offset)

            if city_name:
                has_city, city_obj = self.repository.city_exists(city_name)

                if not has_city:
                    raise ValueError(f"City {city_name} not found.")
                else:
                    city_code = city_obj["code"]
            else:
                city_code = ""

            if state_abbrev:
                if state_abbrev not in STATES_BRAZIL:
                    raise ValueError(f"State {state_abbrev} not found.")

            if cnae_code:
                if not self.repository.get_cnae(cnae_code):
                    raise ValueError(f"CNAE code {cnae_code} not found.")
                
            if zipcode:
                try:
                    zipcode=str(int(zipcode))
                except Exception:
                    raise ValueError(f"Invalid Zipcode {zipcode}.")

            cnpjs_raw_list = self.repository.get_cnpjs_raw(
                state_abbrev=state_abbrev,
                city_code=city_code,
                cnae_code=cnae_code,
                zipcode=zipcode,
                is_all=is_all,
                limit=limit,
                offset=offset,
            )
            cnpj_objs = list(map(cnpj_str_to_obj, cnpjs_raw_list))

            if len(cnpj_objs) != 0:
                cnpjs_info = self.repository.get_cnpjs_info(cnpj_objs)

                return cnpjs_info
            else:
                return {}

        except Exception as e:
            logger.error(f"Error getting CNPJs: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

    async def get_cnpjs_partners(self, cnpj_batch: CNPJBatch):
        """
        Get a list of CNPJ partners information from the database.

        Parameters:
        - cnpj_batch: The batch of CNPJs to search for.

        Returns:
        - A list of CNPJs as dictionaries.
        """
        try:

            cnpj_objs = set(map(cnpj_str_to_obj, cnpj_batch.batch))

            return self.repository.get_cnpjs_partners(cnpj_objs)

        except Exception as e:
            logger.error(f"Error getting CNPJ partners: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

    async def get_cnpjs_company(self, cnpj_batch: CNPJBatch):
        """
        Get a list of CNPJ partners information from the database.

        Parameters:
        - cnpj_batch: The batch of CNPJs to search for.

        Returns:
        - A list of CNPJs as dictionaries.
        """
        try:
            cnpj_objs = set(map(cnpj_str_to_obj, cnpj_batch.batch))

            return self.repository.get_cnpjs_company(cnpj_objs)

        except Exception as e:
            logger.error(f"Error getting CNPJ company: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

    async def get_cnpjs_establishment(self, cnpj_batch: CNPJBatch):
        """
        Get a list of CNPJ partners information from the database.

        Parameters:
        - cnpj_batch: The batch of CNPJs to search for.

        Returns:
        - A list of CNPJs as dictionaries.
        """
        try:
            cnpj_objs = list(map(cnpj_str_to_obj, cnpj_batch.batch))
            est_objs = self.repository.get_cnpjs_establishment(cnpj_objs)

            return est_objs

        except Exception as e:
            logger.error(f"Error getting CNPJ establishment: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

    async def get_cnpj_info(self, cnpj: str):
        """
        Get information about a CNPJ number.

        Parameters:
        - cnpj: The CNPJ number to search for.

        Returns:
        - A dictionary with information about the CNPJ.
        """
        try:
            if not is_number(cnpj):
                raise ValueError(
                    f"CNPJ {cnpj} is not a number. Provide only the 14 digits."
                )

            cnpj_obj = cnpj_str_to_obj(cnpj)

            cnpj_objs = [cnpj_obj]

            cnpj_info = self.repository.get_cnpjs_info(cnpj_objs)
        except Exception as e:
            logger.error(f"Error getting CNPJ info: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

        if not cnpj_info:
            return {"message": f"CNPJ {format_cnpj(cnpj)} not found."}

        return cnpj_info[0]

    async def get_cnpjs_info(self, cnpj_batch: BatchModel):
        """
        Get information about a CNPJ number.

        Parameters:
        - cnpj_batch: The CNPJ batch to search for.

        Returns:
        - A dictionary with information about the CNPJ.
        """
        try:
            cnpj_list = list(set(cnpj_batch.batch))
            cnpj_validity_list = are_cnpj_str_valid(cnpj_list)

            cnpj_validity_dict = dict(zip(cnpj_list, cnpj_validity_list))

            valid_cnpjs = [
                cnpj_str
                for cnpj_str, cnpj_validity_dict in cnpj_validity_dict.items()
                if cnpj_validity_dict["is_valid"]
            ]
            valid_cnpj_objs = list(map(cnpj_str_to_obj, valid_cnpjs))

            invalid_cnpjs = {
                cnpj_str: cnpj_validity_dict
                for cnpj_str, cnpj_validity_dict in cnpj_validity_dict.items()
                if not cnpj_validity_dict["is_valid"]
            }

        except Exception as e:
            logger.error(f"Error getting CNPJ info: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

        return {
            "success": self.repository.get_cnpjs_info(valid_cnpj_objs),
            "fail": invalid_cnpjs,
        }


def get_cnpj_service(repository: CNPJRepository = CNPJRepositoryDependency):
    return CNPJService(repository)


CNPJServiceDependency = Depends(get_cnpj_service)

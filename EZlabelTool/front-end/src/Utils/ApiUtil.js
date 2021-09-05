export default class ApiUtil {
    static URL_IP = 'http://192.168.0.202:5000';
    static URL_ROOT = '/api/v1';
    // API for user
    // static API_LOG_IN = ApiUtil.URL_ROOT + '/log_in' 
    // this login uses flask login module
    static API_LOG_IN = ApiUtil.URL_ROOT + '/login' 
    static API_SIGN_UP = ApiUtil.URL_ROOT + '/sign_up' 
    static API_LOG_OUT = ApiUtil.URL_ROOT + '/logout'

    // API for editor
    static API_EDITOR_ADD = ApiUtil.URL_ROOT + '/add_editor'
    static API_EDITOR_LIST = ApiUtil.URL_ROOT + '/get_editor_list'
    static API_EDITOR_SETTING = ApiUtil.URL_ROOT + '/get_editor_setting'
    static API_EDITOR_SETTING_EDIT = ApiUtil.URL_ROOT + '/editor_setting_edit'
    static API_EDITOR_CHOOSE = ApiUtil.URL_ROOT + '/choose_editor'
    static API_EDITOR_COPY_SETTING = ApiUtil.URL_ROOT + '/get_editor_copy_setting'
    static API_EDITOR_COPY_SETTING_EDIT = ApiUtil.URL_ROOT + '/editor_copy_setting_edit'
    static API_PROJECT_EDITOR_COPY_SETTING = ApiUtil.URL_ROOT + '/get_project_editor_copy_setting'

    // API for labelling
    static API_IMAGE_CHOOSE = ApiUtil.URL_ROOT + '/choose_image'
    static API_LABEL_SUBMIT = ApiUtil.URL_ROOT + '/submit_label'
    static API_LABEL_SKIP = ApiUtil.URL_ROOT + '/skip_label'
    static API_LABEL_BACK = ApiUtil.URL_ROOT + '/back_label'
    static API_LABEL_NEXT = ApiUtil.URL_ROOT + '/next_label'
    static API_IMAGE_VIEW_CHOOSE = ApiUtil.URL_ROOT + '/view_image'

    // API for reviewing
    static API_REVIEW_CHOOSE = ApiUtil.URL_ROOT + '/choose_review_image'
    static API_REVIEW_SUBMIT = ApiUtil.URL_ROOT + '/submit_review'
    static API_REVIEW_NEXT = ApiUtil.URL_ROOT + '/next_review'
    static API_REVIEW_VIEW_CHOOSE = ApiUtil.URL_ROOT + '/view_review_image'

    // API for project
    static API_PROJECT_LIST = ApiUtil.URL_ROOT + '/get_project_list' 
    static API_PROJECT_SEARCH = ApiUtil.URL_ROOT + '/search_project'
    static API_PROJECT_ADD = ApiUtil.URL_ROOT + '/add_project'
    static API_PROJECT_DELETE = ApiUtil.URL_ROOT + '/delete_project'
    static API_PROJECT_SETTING = ApiUtil.URL_ROOT + '/get_project_setting'
    static API_PROJECT_DETAILS = ApiUtil.URL_ROOT + '/get_project_details'
    static API_PROJECT_DETAILS_SEARCH = ApiUtil.URL_ROOT + '/get_project_details_search'
    static API_PROJECT_JOIN_DATASET = ApiUtil.URL_ROOT + '/attach_dataset'
    static API_PROJECT_ROLE_PERMISSION = ApiUtil.URL_ROOT + '/change_role_permission'

    // API for dataset
    static API_DATASET_LIST = ApiUtil.URL_ROOT + '/get_dataset_list' 
    static API_DATASET_SEARCH = ApiUtil.URL_ROOT + '/search_dataset'
    static API_DATASET_ADD = ApiUtil.URL_ROOT + '/add_dataset'
    static API_DATASET_DELETE = ApiUtil.URL_ROOT + '/delete_dataset'
    static API_DATASET_ACTIVE = ApiUtil.URL_ROOT + '/active_dataset'
    static API_DATASET_UPLOAD = ApiUtil.URL_ROOT + '/upload_images'
    static API_DATASET_IMG_DELETE = ApiUtil.URL_ROOT + '/delete_image_in_dataset'
    static API_DATASET_IMAGE_LIST = ApiUtil.URL_ROOT + '/get_images_in_dataset'

    // API for user(member) orgnization level
    static API_USER_LIST = ApiUtil.URL_ROOT + '/get_user_list' 
    static API_USER_SEARCH = ApiUtil.URL_ROOT + '/search_user'
    static API_USER_DELETE = ApiUtil.URL_ROOT + '/delete_user'
    static API_USER_RESET = ApiUtil.URL_ROOT + '/reset_password'
    static API_GET_CURRENT_USER = ApiUtil.URL_ROOT + '/get_current_user'

    // API for upload and download
    static API_UPLOAD = ApiUtil.URL_ROOT + '/upload'
    static API_DELETE = ApiUtil.URL_ROOT + '/delete_image'
    static API_EXPORT = ApiUtil.URL_ROOT + '/export'

}
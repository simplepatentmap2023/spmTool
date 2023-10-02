import streamlit as st

def main():
    items = [1,2,3,4]
    def get_new_values_list():
        st.write(st.session_state['issue'])
    values = st.multiselect('list', items, items, on_change=get_new_values_list, key='issue')
    st.write(values) # < returns correct list

if __name__ == '__main__':
    main()
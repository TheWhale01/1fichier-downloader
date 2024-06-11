export function load({ cookies }) {
	const token: string | undefined = cookies.get('access_token');
	const type: string | undefined = cookies.get('token_type');
	
	return {
		access_token: token,
		token_type: type
	};
}